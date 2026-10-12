# Gap Session 7 Summary — Warden + State Consistency Theorist
## `SCOPE_UPDATED` Rate Limit Design (GAP-27) + A4 Amendment

**Session type:** Gap resolution, multi-specialist (Framework Council — reduced quorum)
**Primary skills:** aisecops-specialist (Warden), state-consistency-theorist
**Baseline spec:** v1.1 + GS1–GS6 amendments
**Session number:** 7 of 10 (gap schedule v3)
**Council constraints honored:** D-CRC-4 (unified ceremony model preserved), GS4 ceremony
authorization entity model (IC-SCOPE-AUTH-1)

---

## Session Scope

Resolve the denial-of-service surface identified in GS3 around the
`SCOPE_HASH_MISMATCH` / `SCOPE_UPDATED` loop. Specifically:

1. Resolve OQ-S-GAP27-1 (per-`agent_id` vs. global vs. per-ceremony-initiator rate limit).
2. Ratify D89 and place `scope_update_min_interval_seconds` at the correct config tier.
3. Register `SCOPE_UPDATE_RATE_EXCEEDED` in Appendix C.
4. Apply A4 amendment to §14.3: escalation threshold 3 → 2 consecutive
   `SCOPE_HASH_MISMATCH`.
5. Absorb GS4's G-S4-N2 (per-CAK rate limiting) into the unified rate-limit model.

Unblocked by GS4 (IC-SCOPE-AUTH-1 ratified; ceremony authorization entity defined as
CAK holder, not the agent being updated).

---

## GAPS RESOLVED

### GAP-27 — Rate Limit on `SCOPE_UPDATED` Events

**Resolution:** Two-layer rate limit model. Primary scope is per-ceremony-initiator
(CAK-holder identity); secondary scope is per-`affected_agent_id`. Both layers must
pass before signature verification executes.

#### D-GAP7-A — Per-ceremony-initiator rate limit is the PRIMARY enforcement layer (OQ-S-GAP27-1 resolution, part 1 of 2)

**Decision:** The primary rate limit is scoped to `ceremony_initiator_id` —
the operator identity associated with the CAK that signed the ceremony payload.
Concretely, the Gate maintains a per-`ceremony_initiator_id` rate-limit state
keyed on the `operator_id` field already present in the IC-SCOPE-AUTH-1
ceremony envelope.

**Warden argument (primary):** GS4 established that ceremony authorization is
rooted in CAK possession, not agent credential possession. The ceremony is an
act of the operator, not of the agent. Rate limiting at the entity that actually
authorizes ceremonies — the CAK holder — directly constrains the abuse vector
(compromised CAK issuing ceremony floods). Per-`agent_id` alone is blind to the
identity of the acting party: the same CAK can target different `agent_id`
values to evade a per-agent window. Per-initiator rate limiting closes this
evasion.

**State Consistency Theorist argument (secondary):** The Ledger-side invariant
is cleaner. `SCOPE_UPDATE_RATE_EXCEEDED` Ledger entries are attributable to
the ceremony initiator, which is a stable, Ledger-persisted identity (CAK
fingerprint / `operator_id`). Per-`agent_id` scoping would require the Gate
to index rate-limit state by a field that is a ceremony *target*, not a
ceremony *actor* — a weaker attribution surface for forensic reconstruction.

**v1.1 operational note:** Because v1.1 registers exactly one CAK
(`genesis-seal.CEREMONY_KEY_ANCHOR`), the per-initiator layer is effectively
global-per-CAK-holder in v1.1. This is accepted: one human operator, one
ceremony throughput budget. Multi-operator / m-of-n CAK (deferred to v2 per
OQ-S-CAK-2) preserves per-initiator semantics — each principal gets its own
budget keyed on `operator_id`.

#### D-GAP7-B — Per-`affected_agent_id` rate limit is a SECONDARY enforcement layer (OQ-S-GAP27-1 resolution, part 2 of 2)

**Decision:** The Gate ALSO maintains a per-`affected_agent_id` rate-limit
window. A ceremony is rejected if EITHER the per-initiator OR the per-agent
window is exceeded.

**Rationale:** Defense in depth against two distinct threat models:
- A compromised CAK targeting a single agent with pathological scope churn
  (e.g., flipping an agent's scope every few seconds to disrupt long-running
  invocations). Per-initiator alone permits this if other agents are not
  being touched — initiator throughput stays under its budget, but a single
  agent experiences starvation.
- A misconfigured operator script iterating scope updates across an agent
  cohort. Per-agent alone catches runaway loops targeting a single agent;
  per-initiator catches fan-out loops.

**Rejection precedence:** If both layers are exceeded, the Gate reports the
per-initiator violation first (more informative for operator triage — the
CAK-holder identity is the actionable piece).

#### D-GAP7-C — Ordering: rate limit check precedes signature verification (ratifies D89 sub-decision)

**Decision:** Both rate-limit layers evaluate BEFORE signature verification.
Cheap checks first; cryptographic work only for requests that cleared rate
limits.

**Rationale:** Prevents signature verification cost from becoming a DoS
amplifier. An attacker sending forged or malformed ceremony payloads at high
volume cannot force the Gate into expensive ECDSA / EdDSA verification work
faster than the rate window allows.

**Side effect:** A rate-exceeded ceremony with an invalid signature produces
only `SCOPE_UPDATE_RATE_EXCEEDED` — the signature invalidity is not observed
because the pathway short-circuits. This is accepted: the Warden's position
is that the rate-exceeded condition is the dispositive failure, and signature
validity of a rate-exceeded ceremony is not operationally meaningful.

#### D-GAP7-D — `scope_update_min_interval_seconds` placed at Tier 3 Anchored Git Config

**Decision:** `scope_update_min_interval_seconds` is NOT a Tier 1 field.
It is specified as a Tier 3 Anchored Git Config parameter in
`<repo_root>/.harness/rate-limits.json` (new file added to Tier 3 inventory).

**Revised provisional defaults:**
- `scope_update_min_interval_seconds_per_initiator`: 60 (1 per minute per operator)
- `scope_update_min_interval_seconds_per_agent`: 3,600 (1 per hour per agent)

**Rationale — why NOT Tier 1:**
- Tier 1 (`genesis-seal.json`) is mint-once at first-boot (§13.2). A Tier 1
  rate limit cannot be tuned without re-bootstrap, which is operationally
  unacceptable for a parameter whose correct value depends on deployment
  tempo. Rollout scenarios (12 agents, coordinated scope migration) may
  require temporary window loosening; incident forensics may require
  temporary window tightening. Both are impossible with Tier 1 placement.

**Rationale — why NOT Tier 2 Sealed Artifact:**
- Tier 2 is reserved for evolving integrity-critical human-authored corpora
  (constitutional suite, Meta-* held-out corpora, write-scope-definitions).
  A rate-limit integer is not a corpus. Creating a sealed corpus for a
  handful of tunable integers is overengineering and obscures the tier
  semantics established in T4.

**Rationale — why Tier 3 IS appropriate:**
- Tier 3 artifacts are Git-committed, change via normal PR workflow, emit
  `CONFIG_UPDATE` Ledger entries on change, and are hash-verified at boot.
  This matches the change frequency (occasional operator tuning) and the
  enforcement model (detect-at-boot) appropriate for an operational
  threshold.
- Modification requires a Git commit, which on a branch-protected
  repository requires PR review — a lightweight human oversight layer
  that matches the parameter's security weight.

**Residual risk accepted:** A malicious Git merge to lower the threshold
to 1 second is detected at the next boot via hash mismatch against the
most recent `CONFIG_UPDATE` Ledger entry, but a running harness with the
malicious value loaded will use it until the next boot. Mitigation:
operators SHOULD configure `SCOPE_UPDATE_RATE_LIMIT_CONFIG_CHANGED`
monitoring (see NEW-GAP-29). v2 consideration: promote rate-limit config
to CAK-ceremony-gated change (OQ-S-GAP27-2, deferred).

#### D-GAP7-E — `SCOPE_UPDATE_RATE_EXCEEDED` registered in Appendix C (SECURITY, sync)

**Ledger entry type:** `SCOPE_UPDATE_RATE_EXCEEDED`
**Category:** SECURITY
**Mode:** synchronous (written before rejection response returns to operator)
**Payload fields:**

| Field | Type | Source |
|---|---|---|
| `ceremony_initiator_id` | string (operator_id from IC-SCOPE-AUTH-1 envelope) | ceremony payload |
| `affected_agent_id` | string OR null (null if per-initiator window tripped before per-agent layer evaluated) | ceremony payload |
| `rate_limit_layer` | enum {`PER_INITIATOR`, `PER_AGENT`} | Gate |
| `attempted_at` | ISO-8601 timestamp | Gate wall-clock |
| `next_eligible_at` | ISO-8601 timestamp | Gate (attempted_at + remaining window) |
| `previous_scope_update_at` | ISO-8601 timestamp (of the `SCOPE_UPDATED` event that started the current window) | Gate rate-limit state |
| `window_seconds` | integer (the configured window that was violated) | Tier 3 config snapshot |
| `ceremony_id` | UUID (per IC-SCOPE-AUTH-1 envelope) | ceremony payload |

**Emission preconditions:** Gate has received a ceremony payload, extracted
`operator_id` and `affected_agent_ids[]`, and determined that the elapsed
time since the most recent `SCOPE_UPDATED` entry for the relevant key is
less than the configured window.

**Response to operator:** Structured rejection payload mirroring the Ledger
entry (without the Ledger-internal integrity fields) so operator tooling
can surface `next_eligible_at` without additional Ledger queries.

---

### A4 Amendment — §14.3 Escalation Threshold (3 → 2)

#### D-GAP7-F — Apply A4-§14.3 amendment

**Previous text (§14.3):**
> "Three consecutive `SCOPE_HASH_MISMATCH` errors for the same invocation →
> Orchestrator escalates to human review queue."

**Revised text (§14.3):**
> "Two consecutive `SCOPE_HASH_MISMATCH` errors for the same `invocation_id`
> → Orchestrator writes `SCOPE_MISMATCH_ESCALATED` (SECURITY, synchronous)
> to the Ledger and escalates to human review queue. Retry budget is NOT
> consumed by the mismatch events themselves; escalation is a separate
> failure classification from retry exhaustion."

**Rationale (ratifies R-S3-1 and D88):**
- A correctly-functioning Orchestrator reads `current_scope_hash` from the
  first mismatch payload and reissues the token against the current hash on
  the first retry. The first retry SHOULD always succeed.
- A second consecutive mismatch after receiving the correct hash indicates
  one of: (a) Orchestrator implementation bug (token issuance not reading
  the mismatch payload correctly), (b) attack (fabricated mismatch payloads
  inducing resource consumption), (c) cache coherency failure between Gate
  and Orchestrator registry. None of these improve with a third retry.
- First mismatch remains INFO-logged (`SCOPE_HASH_MISMATCH_OBSERVED`, no
  escalation). Second mismatch triggers `SCOPE_MISMATCH_ESCALATED`
  (SECURITY, sync — must register in Appendix C alongside
  `SCOPE_UPDATE_RATE_EXCEEDED`).

**Interaction with A5 amendment (signature verification):** No conflict —
A5 governs the signature requirement at `SCOPE_UPDATED` write time; A4
governs escalation on consecutive hash mismatches at retry time. Orthogonal.

---

## GAPS PARTIALLY RESOLVED

None.

---

## GAPS DEFERRED

None from GAP-27's resolved scope. Follow-on OQs (below) deferred by design.

---

## NEW GAPS SURFACED

### NEW-GAP-29 — Aggregate ceremony throughput monitoring
**Domain:** Orchestration Comparativist (primary), Warden (review)
**Description:** Per-initiator and per-agent rate limits handle the cryptographic
authorization boundary. They do NOT address aggregate Ledger write pressure —
Gate processing throughput, Ledger fsync volume, memory footprint of rate-limit
state tables. An orchestrator-layer metric exposing
"`SCOPE_UPDATE` ceremony rate (accepted + rejected) over rolling 5-minute window"
with an alertable threshold is recommended as operational hardening. Not a
cryptographic spec gap; explicitly advisory (C-S-GAP27-advisory).
**Priority:** Medium
**Blocked by:** Orchestrator capability matrix decision on metrics export surface.

### NEW-GAP-30 — Rate-limit state durability across Orchestrator restart
**Domain:** State Consistency Theorist (primary), Warden (review)
**Description:** The per-initiator and per-agent rate-limit windows are
tracked by "elapsed time since most recent `SCOPE_UPDATED` for this key"
— which can be reconstructed from the Ledger at boot. HOWEVER, rate-limit
state that counts REJECTIONS (for future features like rolling-window or
token-bucket enforcement) would need explicit durability semantics. v1.1
uses elapsed-time-based rejection only (no bucket accumulation), so Ledger
replay at boot is sufficient. Documenting the decision: rate-limit state
in v1.1 is derived state, not primary state. This becomes a gap if v2
adopts bucket-based enforcement.
**Priority:** Low (v1.1 fully specified; v2 planning item)

### NEW-GAP-31 — Ceremony_initiator_id attribution under key rotation
**Domain:** Warden (primary), State Consistency Theorist (co-owner)
**Description:** When a `CEREMONY_KEY_ROTATION_COMPLETE` event rotates the
CAK, is the `operator_id` stable across rotation? If the operator_id is
derived from the key fingerprint, rotation changes the id and resets the
per-initiator rate-limit window — giving a rotated operator a fresh
budget. If operator_id is a stable external identity (e.g., an operator
assertion signed by the outgoing CAK during rotation), rotation preserves
the window. Recommendation: operator_id is a stable external identity
bound at first-boot CAK registration and carried forward through rotation.
Requires spec confirmation.
**Priority:** Medium (affects rotation ceremony payload; relevant whenever
rotation is performed)
**Blocked by:** Joint Warden + SCT review; fold into GS4 G-S4-N3 or a
follow-on session if surfaced early.

---

## NEW TENSIONS SURFACED

### T-S7-N1 — Warden ↔ State Consistency Theorist: rate-limit state as derived vs. primary
The per-initiator / per-agent rate-limit windows are, in v1.1, derived from
Ledger replay (elapsed time since most recent relevant `SCOPE_UPDATED`).
State Consistency Theorist's concern: classifying this as derived state
means a Ledger compaction / retention event that removes old `SCOPE_UPDATED`
entries can reset the rate-limit window. If an operator issued
`SCOPE_UPDATED` 58 minutes ago and that entry is compacted between minute
58 and minute 59, the operator's next ceremony sees "no prior
`SCOPE_UPDATED` for this initiator" and accepts immediately rather than
waiting 2 more minutes. Warden's concern: rate-limit state cannot be
dependent on retention boundaries. Proposed resolution: rate-limit window
lookups MUST query both the active Ledger and compaction archives, OR
rate-limit windows MUST be strictly shorter than the minimum retention
window for `SCOPE_UPDATED` entries. Latter is simpler and already likely
true (3600s window << retention for SECURITY/GOVERNANCE entries), but
MUST be made explicit.
**Priority:** High (operational correctness)
**Resolution path:** Add to §14.3 or §13.3 a requirement that
`scope_update_min_interval_seconds_per_*` MUST be strictly less than the
minimum retention window for `SCOPE_UPDATED` Ledger entries. Enforcement:
boot-time validation — if configured window exceeds retention floor,
suspend boot with `RATE_LIMIT_RETENTION_CONFLICT`.

---

## INTERFACE CONTRACTS TOUCHED

- **IC-SCOPE-UPDATE** — AMENDED. Authorization layer (delegated to
  IC-SCOPE-AUTH-1 per GS4) now additionally specifies rate-limit
  precondition. Two-layer rate-limit check (per-initiator, per-agent)
  precedes CAK signature verification. Rate-limit parameters read from
  Tier 3 `rate-limits.json`. Rejection emits `SCOPE_UPDATE_RATE_EXCEEDED`
  (SECURITY, sync).
- **IC-SCOPE-AUTH-1** — NO CHANGE. The ceremony envelope `operator_id`
  field is consumed by the rate-limit layer but no envelope changes
  required.
- No new Interface Contracts introduced.

---

## REFINEMENTS TO EXISTING SPEC TEXT

**R-S7-1 — §14.3 (A4 amendment applied):** Replace "Three consecutive" with
"Two consecutive" per D-GAP7-F. Add `SCOPE_MISMATCH_ESCALATED` (SECURITY,
sync) Ledger entry on the second consecutive mismatch.

**R-S7-2 — §10.9 (A6 amendment refined):** Update the rate-limit language
to reflect the two-layer model. Replace reference to single-window
rejection with the two-layer model; reference Tier 3
`rate-limits.json` for parameter values.

**R-S7-3 — §13.2 (revert A10-related Tier 1 placement for rate limit):**
If A10-adjacent drafts placed `scope_update_min_interval_seconds` in
`genesis-seal.json`, remove. The only Tier 1 scope-update-related field
is `ceremony_authorization_key_anchor` (CAK fingerprint, unchanged from
GS4 D-GAP4-C).

**R-S7-4 — §13.4 (new):** Specify Tier 3 `rate-limits.json` schema:
```
{
  "scope_update_min_interval_seconds_per_initiator": <int>,
  "scope_update_min_interval_seconds_per_agent": <int>
}
```
Boot-time validation rule: both values MUST be strictly less than the
minimum retention window for `SCOPE_UPDATED` Ledger entries
(addresses T-S7-N1).

**R-S7-5 — Appendix C additions:**
- `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, sync) — per D-GAP7-E field list
- `SCOPE_HASH_MISMATCH_OBSERVED` (INFO, sync) — first-occurrence mismatch
  event, no escalation
- `SCOPE_MISMATCH_ESCALATED` (SECURITY, sync) — second-occurrence mismatch
  escalation (D-GAP7-F)
- `CONFIG_UPDATE` annotation: flag `rate-limits.json` as triggering this
  entry type at commit hook
- `RATE_LIMIT_RETENTION_CONFLICT` (GOVERNANCE, sync) — boot suspension
  event (T-S7-N1 mitigation)

**R-S7-6 — Amendment A6 text revision (gap-backlog-v3.md):** Current A6
text specifies per-`agent_id` rate limit with Tier 1 placement. Replace
with two-layer model and Tier 3 placement per D-GAP7-A / D-GAP7-B /
D-GAP7-D. Cross-reference D-GAP7-D for rationale of tier relocation.

---

## DECISION LABELS FOR INTEGRATED SPEC

- **D-GAP7-A** (OQ-S-GAP27-1 part 1): Per-ceremony-initiator rate limit as
  PRIMARY enforcement layer. Absorbs GS4 G-S4-N2.
- **D-GAP7-B** (OQ-S-GAP27-1 part 2): Per-`affected_agent_id` rate limit
  as SECONDARY enforcement layer. Supersedes AG-1's implicit
  per-agent-only closure.
- **D-GAP7-C** (D89 ordering ratification): Rate-limit check precedes
  signature verification.
- **D-GAP7-D** (D89 tier placement): `scope_update_min_interval_seconds_*`
  parameters placed at Tier 3 Anchored Git Config
  (`<repo_root>/.harness/rate-limits.json`), NOT Tier 1.
- **D-GAP7-E** (Appendix C addition): `SCOPE_UPDATE_RATE_EXCEEDED`
  (SECURITY, sync) registered with full field specification.
- **D-GAP7-F** (A4 amendment applied): §14.3 escalation threshold
  3 → 2 consecutive `SCOPE_HASH_MISMATCH`; `SCOPE_MISMATCH_ESCALATED`
  (SECURITY, sync) emitted on second occurrence.

---

## OPEN QUESTIONS DEFERRED

- **OQ-S-GAP27-2** (v2): Should rate-limit config changes require a
  CAK-signed ceremony (promoting from Tier 3 detect-at-boot to Tier 2
  sealed-artifact governance)? Defer: v1.1's Tier 3 model accepted with
  documented residual risk; v2 candidate if operational experience shows
  config-tampering incidents.
- **OQ-S-GAP27-3** (v2): Rolling-window or token-bucket rate limiting
  (vs. v1.1's elapsed-time-since-last-event model)? Defer: v1.1 model is
  sufficient for the threat surface identified; token-bucket adds state
  durability requirements (NEW-GAP-30).

---

## CARRY-FORWARD TO NEXT SESSION

**Inputs to next gap session (GS8):**
- T-S7-N1 (rate-limit window vs. retention floor) — State Consistency
  Theorist must formalize the retention-floor invariant in the Ledger
  retention spec. Candidate for GS8 if SCT is convened; otherwise fold
  into integration pass.
- NEW-GAP-29 (aggregate throughput monitoring) — Orchestration
  Comparativist, medium priority. Fold into orchestrator capability
  matrix refinement.
- NEW-GAP-31 (operator_id stability across CAK rotation) — joint Warden +
  SCT review. May warrant a short dedicated pass or fold into GS4
  follow-on work on G-S4-N3 (break-glass channel).

**Unblocked by this session:**
- A4-§14.3 amendment → ready for integration pass (status: APPLIED).
- A6-§10.9 amendment → revised per R-S7-6; ready for integration pass.
- A7-Appendix-C — `SCOPE_UPDATE_RATE_EXCEEDED` definition now complete;
  field spec available for integration.
- D89 provisional → FINALIZED as D-GAP7-A/B/C/D.
- GS4 G-S4-N2 (per-CAK rate limiting) → CLOSED, absorbed into D-GAP7-A.

**Status updates for gap backlog v3 → v4:**
- GAP-27 → ✅ Resolved (D-GAP7-A through D-GAP7-F)
- GS4 G-S4-N2 → ✅ Closed (absorbed into GAP-27 resolution)
- AG-1 closure annotation → supersede: the per-agent scope from GS3 D89
  is now the SECONDARY layer, not the sole layer; update backlog
  annotation accordingly.
- A4-§14.3 amendment → ✅ Applied
- A6-§10.9 amendment → Revised; status remains Outstanding pending
  integration pass with R-S7-6 text.
- A7-Appendix-C → expand pending entry list to include
  `SCOPE_MISMATCH_ESCALATED`, `SCOPE_HASH_MISMATCH_OBSERVED`,
  `RATE_LIMIT_RETENTION_CONFLICT`.

**New entries for gap backlog:**
- NEW-GAP-29 (aggregate ceremony throughput monitoring) — Medium
- NEW-GAP-30 (rate-limit state durability across restart) — Low, v2 item
- NEW-GAP-31 (operator_id stability across CAK rotation) — Medium

**Tension map updates:**
- T-S7-N1 → add as active tension; priority High; resolution path
  documented in R-S7-4.

---

## Session Close

GAP-27 is fully resolved with a two-layer rate-limit model that honors
GS4's ceremony authorization entity semantics (per-initiator primary) while
preserving the operational value of per-agent scoping (secondary, against
targeted agent-scope churn). The `scope_update_min_interval_seconds_*`
parameters are placed at Tier 3 Anchored Git Config, not Tier 1 — the
mint-once property of Tier 1 is incompatible with tuneable operational
thresholds. A4 amendment applied. `SCOPE_UPDATE_RATE_EXCEEDED` and two
companion Ledger entry types registered. One new cross-domain tension
(T-S7-N1) and three new gaps (NEW-GAP-29/30/31) surfaced and routed.
