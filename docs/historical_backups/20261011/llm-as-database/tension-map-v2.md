# LLM as Database: Agent Harness Architecture
## Cross-Domain Tension Map v2.0

> **Supersedes:** `tension-map-v1.md`
> **Source documents:** `llm-as-database-v1_1-integrated-spec.md`,
>   `tension-map-v1.md`, Council Review Checkpoint — Post-Gap Sessions 1–3
> **Sessions:** Session 7 (T1–T12), Gap Sessions 1–3 (T13–T14)
> **Tensions tracked:** 14 working-session tensions + 6 pre-mapped structural tensions
> **Last updated:** Council Review Checkpoint, Post-GS3

---

## Reading Guide

Tensions in this document are drawn from three sources:

1. **Session 7 spec resolutions (T1–T12)** — decisions the council worked to resolution
   during Session 7, each producing one or more Interface Contracts and decision numbers.
2. **Gap session tensions (T13–T14)** — new cross-domain tensions surfaced during Gap
   Sessions 1–3 and promoted to the tension map by the Post-GS3 Council Review Checkpoint.
3. **Pre-mapped structural tensions (Pre-T1 through Pre-T6)** — six tensions baked into the
   council skill before Session 1. A cross-reference section maps how each was addressed.

Tension numbering: T1–T12 follow Session 7's Appendix F cross-reference. T13–T14 are
assigned sequentially by the Post-GS3 checkpoint. Pre-T labels are fixed.

Status labels:

| Status | Meaning |
|--------|---------|
| ✅ **Resolved** | Fully specced; no open questions remain |
| 🔶 **Partial** | Core decision made; one or more policy or empirical questions remain open |
| ⚠️ **Partial (structural gap)** | Core mechanism described but key contractual element unspecced |
| 🔴 **Open** | Active tension; no resolution made; gap session required |
| ⚠️ **Unlocatable** | Referenced in spec index but body text not located |

---

## Session 7 Tensions (T1–T12)

---

### T1 — `attention_weight` Authority
**Graph Data Architect vs. MEMIT Specialist**

**Status:** ✅ Resolved

**The conflict:** `attention_weight` in the original `.larql` format was agent-authored.
The Graph Data Architect wanted it as a schema-layer intent declaration. The MEMIT Specialist
objected: `attention_weight` is computed by MEMIT's covariance balancer during compile —
letting agents author this number is a category error that could produce incorrect validation
gating.

**Resolution:** Split into two separate concepts (§8.6, closes OQ-W5):
- `declared_importance` — agent-authored enum: `CORE` / `SUPPORTING` / `INCIDENTAL`.
  Reference mappings: 0.9 / 0.7 / 0.4. Used pre-commit by the Validator to gate
  verification intensity.
- `attention_weight` — engine-computed during MEMIT compile. Not authored by any agent.
  Emitted to the State Ledger for audit only.

A post-compile divergence check flags soft signals for human review (CORE yields
`attention_weight < 0.5`, or INCIDENTAL yields `> 0.9`). Not a hard rejection.

**Remaining open question:** None. OQ-W5 closed.

**Interface contracts:** `.larql` format extended; `IC-SC1` `CONTENT_CLASSIFICATION`
directive added. `attention_weight` field is engine-output-only.

---

### T2 — TGA Independence vs. Correctness Depth
**Validation Contract Architect vs. Orchestration Comparativist**

**Status:** ✅ Resolved

**The conflict:** The Validation Contract Architect required the Test-Generation Agent (TGA)
to never see the Coder Agent's code before writing tests — independence enforced by sequencing.
The Orchestration Comparativist noted this produces a scalability problem: human-authored test
suites become a bottleneck, and blind TGA tests may have poor coverage.

**Resolution:** Four-layer TGA validation cascade (§9.4, closes OQ-V3):
- **L1 — Structural check** (all outputs, mandatory): ≥2 assertions per test, no bare `pass`.
- **L2 — Stub probe** (all outputs, mandatory): TGA tests run against empty stub; tests that
  pass the stub are false positives — TGA is re-invoked.
- **L3 — Dual-TGA** (`CORE` tasks only): two independent TGA invocations; only behaviors
  asserted by both count as active gates.
- **L4 — Meta-TGA** (every 50 commits or weekly): held-out corpus per Sealed Corpus pattern.

Independence enforced by sequencing and stub probe, not policy alone. Dual-TGA scoped to
CORE tasks to address the Orchestration Comparativist's scale concern.

**Remaining open question:** None at structural level. OQ-V5 (corpus authorship cadence for
Meta-TGA) is addressed separately in T3.

**Interface contracts:** IC-V-TGA1, IC-V-TGA2.

---

### T3 — Meta-* Audit Completeness vs. Corpus Integrity
**Warden vs. Validation Contract Architect**

**Status:** 🔶 Partial

**The conflict:** The Warden needed complete audit visibility into Meta-Validator and Meta-TGA
health monitoring behavior — specifically, per-case outcome logging, not just aggregate scores.
The Validation Contract Architect needed held-out corpora protected from Validator / TGA access
during normal operation (exposure would allow agents to overfit to held-out cases, corrupting
the health signal).

**Resolution:** Sealed Corpus pattern applied to both Meta-* corpora (§13.3):
- Held-out corpora are Tier 2 sealed artifacts: versioned additive directories, operator-signed
  manifests, dual-store integrity verification.
- Access is time-bounded: corpora accessible only during scheduled Meta-* runs.
- Per-case audit reporting is mandatory. Aggregate-only reporting is explicitly forbidden.

**Remaining open question (OQ-V5):** Who has authority to author new corpus cases? At what
cadence must the corpus be extended to prevent Health Score overfitting? What constitutes a
held-out case (format)? Minimum corpus size before a Meta-* run produces a meaningful score?

**Interface contracts:** IC-SL7, IC-SL8, IC-SL9.

---

### T4 — Configuration Authority Fragmentation
**Warden vs. State Consistency Theorist vs. Orchestration Comparativist**

**Status:** ✅ Resolved

**The conflict:** Three separate sessions had specced three different storage patterns for
configuration artifacts, each with different trust requirements:
- Warden: permanently immutable Genesis seal (D49, dual-store).
- State Consistency Theorist: path-classification as an anchored Git artifact (D76).
- Orchestration Comparativist: agent YAMLs as Git-committed operational config.
Write Scope Definitions needed to be agent-runtime-immutable but operator-updatable. These
four patterns had no unified governance model.

**Resolution:** Three-tier `.harness/` model (§13, closes OQ-GOC1 via D76):
- **Tier 1 — Immutable Anchor:** Mint-once, verify-forever. `genesis-seal.json` and
  `orchestrator-key-anchor.json`. Dual-stored (Ledger primary + `.harness/` secondary).
  Boot-time hash comparison; mismatch suspends boot.
- **Tier 2 — Sealed Artifacts:** Evolving human-authored integrity-critical artifacts.
  Versioned additive directories, operator-signed manifests.
- **Tier 3 — Anchored Git Config:** Git-committed operational config with Ledger anchoring.
  Detect-at-boot integrity enforcement.

Agent YAML is bound to its Write Scope Definition via hash. Update ceremony scales with
blast radius.

**Remaining open question:** None at structural level. Stronger Tier 3 enforcement
(pre-receive server-side Git hooks) is deferred to v2.

**Interface contracts:** IC-CFG1, IC-CFG2, IC-CFG3.

---

### T5 — Token Revocation vs. In-Flight Write Continuity
**Warden vs. Orchestration Comparativist**

**Status:** 🔶 Partial → *Updated Post-GS3: structural resolution confirmed (D87, closes OQ-S4)*

**The conflict:** The Warden needed immediate bulk revocation capability for compromised agents.
The Orchestration Comparativist needed agent invocations to complete without mid-flight
interruption. Short TTLs alone don't solve this: a token can expire after 2PC Phase 1 but
before Phase 2 completes.

**Resolution:** Two mechanisms combined (§10.4, §10.5, closes OQ-S2, OQ-S6):
- **Agent suspension model:** `suspended_agents` in-memory set on Orchestrator. Suspended
  agents cannot receive new tokens; presented tokens are rejected at Gate with
  `TOKEN_AGENT_SUSPENDED`. Suspension is immediate.
- **Governance-state binding:** Tokens carry hash-bindings to Write Scope Definition version
  and Agent YAML version at issuance. Stolen token becomes invalid the moment any bound
  governance document changes within the TTL window.
- **Orchestrator signing key dual-store:** Public half stored in both Ledger
  (`ORCHESTRATOR_KEY_ANCHOR`, immutable) and `.harness/orchestrator-key-anchor.json`.
  Boot-time hash comparison; mismatch suspends boot.

**OQ-S4 closure (Post-GS3):** D87 resolves the scope update serialization question.
Forward-only semantics for PREPARED transactions are the core resolution: a scope change does
not interrupt a write already in the PREPARED state; post-update tokens enforce the new scope;
Gate rejections due to scope hash mismatch are classified as infrastructure failures (no retry
budget consumed). OQ-S4 is closed.

**Residual seams (not reopenings of T5):** GAP-25 through GAP-28 (canonical) are seams in
the D87 implementation — Ledger → registry propagation window, ceremony authorization model,
rate limit specification, and proactive notification obligation.

**Remaining open question:** Full PKI (mass revocation lists, Orchestrator key rotation,
multi-Orchestrator trust) deferred to v2. T14 (ceremony authorization key model) is a new
adjacent tension; see below.

**Interface contracts:** IC-CFG3 (YAML binding check), boot-time verification sequence
(§13.5 steps 3 and 6), IC-SCOPE-UPDATE, IC-SCOPE-RATE-1, IC-SCOPE-AUTH-1 (D87–D90).

---

### T6 — Genesis Completeness vs. Catastrophic Forgetting Risk
**Graph Data Architect vs. MEMIT Specialist**

**Status:** 🔶 Partial

**The conflict:** The Graph Data Architect wanted Genesis to be comprehensive — bake in all
foundational knowledge upfront. The MEMIT Specialist warned that over-encoding at Genesis
is expensive to correct and degrades MEMIT's locality guarantees.

**Resolution:** Three-part model (§8.7, §8.8):
- **Genesis scope test:** "Is the harness broken without this fact? If no, it does not belong
  in Genesis."
- **Drift-from-anchor model:** Drift measured relative to most recent anchor event; resets to
  zero after anchor. Correction costs are explicit and bounded.
- **Architect capacity model:** Hard security cap of 10,000 edges per patch; MEMIT-recommended
  sub-batch of 2,000 edges. Both ceilings enforce MEMIT's locality constraint.

**Remaining open question (OQ-W1):** All threshold values (drift warning 1,500, drift hard
trigger 8,000, sub-batch 2,000) are provisional heuristics pending empirical validation
against target model architecture.

**Interface contracts:** IC-MEMIT-3 (`ANCHOR_ESTABLISHED` flag on qualifying Ledger entries).

---

### T7 — Schema Migration Token Timing
**Warden vs. State Consistency Theorist**

**Status:** ✅ Resolved → *Updated Post-GS3: OQ-TPC1 closed by D85*

**The conflict:** Schema migration token had a 30-minute TTL from issuance to Genesis compile
completion. Large Genesis patches could easily exceed 30 minutes. TTL expiry mid-compile
produces indeterminate state: `PREPARED` entry written, but token now invalid.

**Resolution:** Admission-time TTL model (§10.6, §14.1, revises D27):
- Token TTL is 10 minutes, measured to 2PC Phase 1 admission only.
- Token is consumed at the moment the Commit Executor writes the `PREPARED` Ledger entry.
- Once admitted, compile proceeds independent of subsequent token state.

**OQ-TPC1 closure (Post-GS3):** D85 resolved the PREPARED-state timeout question. Two-value
timeout model: `incremental_prepared_timeout` (default 2 hours) for standard writes;
`genesis_prepared_timeout` (no default — operators size to target model and patch volume)
for Genesis writes. Genesis timeouts trip the circuit breaker; auto-compensation is prohibited
where no prior `COMMITTED` overlay exists to revert to. OQ-TPC1 is closed.

**Residual (not a reopening of T7):** GAP-23 (canonical) — Genesis Hold lifecycle through
the reset ceremony is unspecced. Specifically: whether Hold release is a precondition for
the reset ceremony, and whether `CIRCUIT_RESET` implicitly releases active Holds from the
failed Genesis transaction.

---

### T8 — Write Lock Semantics Conflation
**State Consistency Theorist vs. Orchestration Comparativist**

**Status:** ✅ Resolved

**The conflict:** The original D59/D60 scope lock conflated three distinct concerns: preventing
concurrent writes to the same model region (a MEMIT locality concern), preserving the
dependency context of a long-running task (a correctness concern), and preventing Pruning from
removing edges a task is actively using (a Pruning interaction concern).

**Resolution:** Lock / Hold split (§11.12, §17.3, closes OQ-CW1 partially):
- **Write Lock** (60-minute TTL, auto-release): Placed on the *write target region* during
  active write operations. Blocks concurrent agent writes to same region. Does not block reads
  or Pruning of non-targeted regions.
- **Dependency Hold** (72-hour TTL, renewable on escalation): Placed on edges the task is
  *reading*. Blocks Pruning operations on held edges only.

**Remaining open question (OQ-CW1):** Voluntary Write Lock release before TTL expiry and
inter-agent negotiation for overlapping write regions are deferred to v2.

**Interface contracts:** IC-PA7 (Pruning → Orchestrator: Hold-state query).

---

### T9 — Compaction Correctness vs. Efficiency
**MEMIT Specialist vs. Validation Contract Architect**

**Status:** 🔶 Partial

**The conflict:** The MEMIT Specialist preferred delta composition for compaction efficiency.
The Validation Contract Architect objected: delta composition skips MEMIT's orthogonal
projection and covariance balancer steps for already-compiled layers, weakening the
mathematical guarantees the write engine's safety properties depend on.

**Resolution:** Full MEMIT re-run mandated (§11.14, §8.10). Delta composition rejected on
correctness grounds. Every compaction is a Genesis-Mode MEMIT recompile on all active
`.larql` patches. Epoch bundling for storage management (superseded patches → compressed
manifest-sealed archive bundles).

**Remaining open question (OQ-OC3):** Compaction verification sample size ("100% CORE +
10% random others" is a starting heuristic). Sampling methodology and Behavioral Probe
failure report format to TC are unspecced.

**Interface contracts:** IC-OC6, IC-OC7, IC-OC8.

---

### T10 — Out-of-Band Git Commit Handling
**State Consistency Theorist vs. Warden**

**Status:** ✅ Resolved

**The conflict:** Humans and external tools can commit to Git outside the harness pipeline.
State Consistency Theorist needed detect-and-reconcile. Warden could not allow auto-compilation
of catch-up patches from unauthenticated state changes. These requirements were in direct
conflict.

**Resolution:** Two-queue model with distinct semantics (§15):
- Out-of-band commits detected by Pruning Agent; catch-up patches flagged
  `requires_human_review` — no auto-compile under any condition.
- Catch-up patches route to the Reconciliation Review Queue (distinct from Correctness
  Review Queue). Available decisions: `approve_patch` | `reject_patch` | `modify_patch` |
  `defer_with_reason`. `modify_patch` outputs re-enter the standard Validator cascade.
- Default on neglect differs by queue: Correctness Review → task times out into logged
  suspension. Reconciliation Review → items accumulate; backlog signals escalate.

**Remaining open question:** None at structural level. Backlog threshold values are starting
heuristics.

**Interface contracts:** IC-PA8, IC-OR10, IC-OR11, IC-OR12, IC-OR13, IC-OR14.

---

### T11 — Audit Trail vs. State Ledger Consolidation
**Warden vs. State Consistency Theorist**

**Status:** 🔶 Partial

**The conflict:** The Warden had specced a separate, cryptographically immutable audit trail
(D28) as a security artifact. The State Consistency Theorist had separately specced a State
Ledger as the primary consistency record. These were two append-only Merkle-chain integrity
logs doing substantially overlapping work.

**Resolution:** Unified Ledger — one artifact, two query lenses (§16):
- One append-only JSONL file at `<harness_root>/.state-ledger/ledger.jsonl`.
  Merkle-chain-lite integrity. Outside Git and outside `.vindex`.
- "Audit trail" is an `audit_category` tag on Ledger entries (SECURITY, CONSISTENCY,
  VALIDATION, GOVERNANCE, LIFECYCLE), not a separate store.
- Three-tier writer model (W1 / W2 / W3). Sync/async write mode split: security-critical
  entries are synchronous (blocking); observation entries are async via WAL — guaranteed
  delivery, never lossy, not on the commit critical path.
- Tiered read access by role.

**Post-GS3 note:** GS2 and GS3 introduced four new synchronous Ledger entry types
(`SCOPE_UPDATE_RATE_EXCEEDED`, `SCOPE_MISMATCH_ESCALATED`, `DEPENDENCY_HOLD_RELEASED_SIGNED`,
`HOLD_RELEASE_REJECTED`). All are correctly categorized as synchronous under the existing
resolution framework (GOVERNANCE and SECURITY class events). The sync/async split is holding.
The State Consistency Theorist confirmed no new entries require Merkle-chain-lite structure
changes beyond standard append-only chaining. No new tension introduced.

**Remaining open question (OQ-SL1):** Full Ledger retention policy. WAL flush cadence is an
unspecified heuristic. Operator retention override governance is unspecced.

**Interface contracts:** IC-LDG1 through IC-LDG5.

---

### T12 — Referenced in Appendix F — Body Text Not Located
**Specialists unknown**

**Status:** ⚠️ Unlocatable

Appendix F states "T1–T12: Session 7 (Integration — cross-domain resolutions)." Eleven
tensions (T1–T11) are traceable to named spec sections, Interface Contracts, and decision
closures. T12 does not appear with an explicit label in any reviewed spec body section.

**Candidate tensions (from tension-map-v1.md):**
- Peer agent review authorization model during D37 Step 2 escalation.
- W3 emergency writer scope (Warden vs. State Consistency Theorist).
- `CONTENT_CLASSIFICATION mixed` rejection protocol — who tells the Coder Agent to split a
  mixed-content patch?

**Council action:** T12 identification remains an open item for the next full council session.
No candidate tension is promoted here; none was worked to resolution. Status unchanged.

---

## Gap Session Tensions (T13–T14)

*These tensions were surfaced during Gap Sessions 1–3 and promoted to the tension map by the
Post-GS3 Council Review Checkpoint (D-CRC-5, D-CRC-6).*

---

### T13 — Advisory Boundedness vs. Operational Flexibility
**MEMIT Specialist vs. Orchestration Comparativist**

**Status:** 🔴 Open — gap session required before Phase 2 can close

**Surfaced in:** Gap Session 1 (T-NEW-1)
**Promoted by:** Council Review Checkpoint, Post-GS3 (D-CRC-5)
**Blocks:** GAP-3 v2 spec block 2c ratification; Phase 2 exit criteria

---

**The conflict:**

The `LARQL_VERSION_LEGACY` advisory state exists to allow agents operating on an older `.larql`
schema version to continue functioning during a bounded migration window while the team
ratifies a migration manifest and advances to the new version.

> *Quick context:* When the `.larql` patch format changes version, existing agents may still
> produce patches in the older format. Rather than hard-blocking them immediately, the system
> enters `LARQL_VERSION_LEGACY` advisory state — a grace period during which old-format patches
> are still accepted but translated via the `larql_migration_manifest`. The advisory state is
> meant to be temporary.

🔬 **MEMIT Specialist requires:** `LARQL_VERSION_LEGACY` must be a strictly bounded transition
state, not an indefinite production configuration. Unbounded legacy-patch accumulation creates
three compounding problems: (1) translation debt in the manifest grows with each accumulated
patch; (2) compaction fidelity degrades because translated patches carry an additional
approximation layer (the float-to-enum bucket boundary decision introduces lossy rounding);
(3) manifest maintenance burden grows indefinitely. The three-tier accumulation escalation
model (10 patches → warning, 50 → soft-block, 100 → hard-block) in v2 outline spec block 2c
is a structural proposal. The hard-block ceiling of 100 patches is unanchored — there is no
empirical data establishing at what accumulation count compaction fidelity meaningfully
degrades for a given model architecture.

🔀 **Orchestration Comparativist requires:** Teams in active development cannot be hard-blocked
mid-sprint by an elapsed notice period. If a team is mid-delivery and the legacy accumulation
counter hits the hard-block threshold, agents lose the ability to write — creating an
unplanned project halt with no predictable recovery path. The orchestration layer needs: (a)
predictable enforcement timing so sprint planning can account for the migration window; (b) an
operator override mechanism that allows extension without disabling enforcement entirely.

**Why this matters:** The current spec block 2c proposes a hard-block at 100 accumulated
legacy patches. If this number is too low (fidelity is actually fine at 100), teams are
disrupted unnecessarily. If it is too high (fidelity degrades at 40 patches), the spec
allows dangerous accumulation. Without GAP-1 empirical data, neither side can commit.

**Resolution path:** The MEMIT Specialist must provide either the empirical degradation rate
(from GAP-1 resolution) or a principled proxy — a conservative ceiling justified by the
structure of the translation approximation rather than observed fidelity. The Orchestration
Comparativist must specify the minimum operator override window needed to preserve sprint
continuity. The `LEGACY_EXTENSION_GRANTED` mechanism (OQ-GAP1-3) is the candidate — a signed
exception record that allows the operator to extend past the hard-block with an explicit
acknowledgment of the compaction fidelity risk.

**Pre-mapped tension check:** T13 is adjacent to **Pre-T2** (Write Volume vs. Edit Locality)
in that both concern the effect of write volume on MEMIT fidelity. T13 is distinct: its
primary domain is governance enforcement policy (when to hard-block) rather than the technical
capacity model (how many edges fit). Pre-T2's resolution (write budget and drift anchoring)
does not address the operational flexibility dimension. T13 requires its own resolution.

**Open questions:**
- `OQ-GAP1-3` (carry-forward): Should the hard-block allow operator extension with a signed
  exception record (`LEGACY_EXTENSION_GRANTED` pattern)?
- `OQ-GAP1-4` (carry-forward): At what accumulation count does compaction fidelity
  meaningfully degrade? (Blocked by GAP-1 empirical resolution.)

**Required gap session:** MEMIT Specialist + Orchestration Comparativist

---

### T14 — Single-Key vs. Dual-Key for Ceremony Authorization
**Warden vs. Orchestration Comparativist**

**Status:** 🔴 Open — gap session required; can be combined with GAP-26 resolution

**Surfaced in:** Gap Session 3 (implicit in OQ-S-GAP25-3 / canonical OQ-S-GAP26-3)
**Promoted by:** Council Review Checkpoint, Post-GS3 (D-CRC-6)
**Blocks:** GAP-26 resolution; D90 implementation planning; unified ceremony authorization
model (D-CRC-4)

---

**The conflict:**

D90 (Gap Session 3) established that scope update ceremonies must be verified against a
"declared ceremony authorization key" before the Orchestrator writes a `SCOPE_UPDATED` Ledger
entry. The question is what kind of key that is and whether it is separate from the key the
Orchestrator already holds.

> *Quick context:* At first boot (§10.5), the Orchestrator generates an asymmetric signing
> key. The public half is anchored in both the State Ledger and `.harness/orchestrator-key-anchor.json`
> (Tier 1, immutable). This key currently authorizes the Orchestrator to sign tokens and
> produce certain Ledger entries. The question is whether this same key can also authorize
> governance ceremonies — or whether ceremonies require a separate, human-held key.

🛡️ **Warden requires:** The ceremony authorization key must be separate from the Orchestrator's
first-boot key, and must be held by a human operator, not by the Orchestrator itself. The
reasoning: if the Orchestrator is compromised, a single-key model allows the compromised
Orchestrator to authorize its own scope changes — expanding its own write authority, approving
its own Hold releases, or resetting its own circuit breaker. Governance ceremonies are
precisely the operations a compromised Orchestrator would want to execute without human
oversight. A separate human-held key severs this authorization path. The Warden notes that
this requirement applies to all three ceremony types identified in GS1–3: migration manifest
ratification (GS1, D-GAP1-B), Hold release (GS2/GS3, GAP-21 canonical), and scope update
ceremonies (GS3, D90). The ceremony authorization model must be unified (D-CRC-4).

🔀 **Orchestration Comparativist requires:** A separate human-held ceremony key introduces
operational overhead the spec must honestly account for. The key must be: (a) physically
secured in a location known to on-call operators; (b) accessible during incidents, which may
occur outside business hours; (c) rotated on a defined cadence with archival of the prior key
material; (d) registered with the harness in a way that doesn't require harness write access
to update. Key unavailability during a ceremony blocks the ceremony indefinitely. For the
circuit breaker reset ceremony specifically, key unavailability during an incident means the
system remains in READ_ONLY mode until a keyholder is reached. The Orchestration Comparativist
is not arguing against separation — the Warden's threat model is correct — but the operational
cost must be specified, not assumed away.

**Why this matters:** The ceremony authorization model is the trust foundation for every
governance-class operation in the system. If the key model is wrong, all three ceremony types
are potentially exploitable. If the operational overhead is unspecified, operators will
improvise workarounds that are more dangerous than a well-designed single-key model would
have been.

**Resolution path:** The Warden must specify the minimum physical storage contract for a
separate ceremony authorization key — the four required fields: storage medium, governance
tier, retention rule, write authority. The Orchestration Comparativist must specify what
operational overhead is acceptable given the threat model. The candidate resolution is a key
hierarchy: Orchestrator key for operational writes; a separate human-held key for governance
ceremonies; the human-held key registered in a Tier 1 artifact (read-only to the harness) at
first-boot setup, not at runtime. This makes the human-held key a boot-time configuration
fact rather than a runtime-writable parameter, which severs the Orchestrator's ability to
register its own ceremony authorization key.

**Pre-mapped tension check:** T14 maps closely to **Pre-T1** (Immutability vs. Mutability
Window). Pre-T1 was resolved by defining a mutability lifecycle with GOVERNANCE-class gates.
T14 is the sub-question of what authorizes a GOVERNANCE-class gate action — a question Pre-T1
does not answer. The Warden and State Consistency Theorist are both Pre-T1's primary voices;
the Warden is T14's primary voice with the Orchestration Comparativist as the secondary. The
overlap is structural, not a routing conflict.

**Open questions:**
- `OQ-S-GAP26-1` (canonical): Where is the operator signing key for scope update ceremonies
  stored, and under what physical storage contract? (Four required fields: storage medium,
  governance tier, retention rule, write authority.)
- `OQ-S-GAP26-2` (canonical): Retention policy and rotation cadence for operator signing
  key material?
- `OQ-S-GAP26-3` (canonical): Must ceremony authorization key be separate from Orchestrator
  first-boot key (§10.5)? This is the core T14 question.

**Amendment dependency:** IC-TC-RESET (circuit breaker reset ceremony) must receive a
placeholder noting its ceremony authorization key model depends on T14 / GAP-26 resolution
(C-CRC-2). The reset ceremony and the scope update ceremony must use the same key model once
T14 is resolved.

**Required gap session:** Warden + Orchestration Comparativist — combinable with GAP-26
resolution (GS4)

---

## Pre-Mapped Structural Tensions — Session 7 Disposition

*Updated post-GS3 where relevant.*

---

### Pre-T1: Immutability vs. Mutability Window
**Warden vs. State Consistency Theorist**

**Session 7 resolution:** Addressed by T5 (signing key dual-store + token model) and T11
(sync/async Ledger write mode). Mutability lifecycle is fully defined:
- Tier 1 artifacts: immutable from mint.
- Active `.vindex` overlay: mutable during Phase 1 prepare window (2PC `PREPARED` state).
- `.vindex` post-Phase 2: effectively immutable — superseding requires a new `COMMITTED`
  entry; prior overlay is archived, not overwritten.
- Genesis tiers L1–L2: frozen post-mint via `IMMUTABLE_ANCHOR`. L4 updatable via standard
  pipeline.

**Post-GS3 update:** T14 (ceremony authorization key model) is the governance-layer sub-question
of Pre-T1 — specifically, what authorizes a transition out of an effectively-immutable state
via a GOVERNANCE ceremony. Pre-T1's mutability lifecycle is sound; T14 does not reopen it.

**Status:** ✅ Fully resolved (via T5, T11). T14 is an adjacent open tension.

---

### Pre-T2: Write Volume vs. Edit Locality
**Graph Data Architect vs. MEMIT Specialist**

**Session 7 resolution:** Addressed by T6 (drift-from-anchor model + Architect capacity
model). Capacity ceiling (10,000 edge hard cap, 2,000 sub-batch recommendation) and
drift-from-anchor triggers protect MEMIT's locality guarantee without capping total knowledge
encoded over time.

**Post-GS3 update:** T13 is adjacent — both concern the effect of write volume on MEMIT
fidelity. T13 is a governance enforcement question (when to hard-block legacy accumulation);
Pre-T2's resolution addresses the structural capacity model, not enforcement policy.

**Status:** 🔶 Structurally resolved. All threshold values (1,500 / 8,000 / 2,000) remain
provisional pending empirical validation (OQ-W1 — GAP-1 formally deferred to implementation
phase). T13 is an adjacent open tension.

---

### Pre-T3: Validator Independence vs. Test Coverage at Scale
**Validation Contract Architect vs. Orchestration Comparativist**

**Session 7 resolution:** Addressed by T2 (TGA four-layer cascade). Independence is enforced
by sequencing and the stub probe. Coverage depth is achieved through dual-TGA for CORE-
importance tasks only.

**Status:** ✅ Fully resolved (via T2). No post-GS3 updates.

---

### Pre-T4: Audit Completeness vs. Write Throughput
**Warden vs. State Consistency Theorist + MEMIT Specialist**

**Session 7 resolution:** Addressed by T11 (unified Ledger with sync/async write mode split).
Security-critical entries are synchronous (blocking); observation entries are async via WAL
with guaranteed delivery.

**Post-GS3 update:** GS2 and GS3 introduced four new synchronous entry types. All are
correctly GOVERNANCE or SECURITY class under the existing framework. The sync/async split
continues to hold. No new tension. Pre-T4 status unchanged.

**Status:** 🔶 Structurally resolved. WAL flush cadence is an unspecified heuristic (part
of GAP-14 in the gap backlog).

---

### Pre-T5: Schema Stability vs. Agent Autonomy
**Graph Data Architect vs. Orchestration Comparativist**

**Session 7 resolution:** Partially addressed by T4 (three-tier config governance). Gate's
scope check enforces declared relation vocabulary at runtime. Write Scope Definitions in
Tier 2 seal per-agent relation authority.

**Post-GS3 update:** GS1 improved the versioning sub-gap of Pre-T5 by producing v2 outline
spec blocks for GAP-3 (deprecation ceremony, migration manifest authorship, advisory window
policy). These address the version transition machinery. The schema extension *proposal*
pathway — the mechanism by which agents could propose new relation types for Warden / human
approval — remains unspecced. Pre-T5 status unchanged.

**Status:** ⚠️ Partially resolved. Agents are prevented from using undeclared relations at
runtime. The authorized schema extension pathway for proposing new relation types is not
contractually defined. Carried as a sub-gap within GAP-3.

---

### Pre-T6: Genesis Completeness vs. Genesis Lock-in
**Graph Data Architect vs. MEMIT Specialist**

**Session 7 resolution:** Addressed by T6 (minimal viable Genesis scope test + four-tier
structure + drift-from-anchor model). The four-tier structure allows comprehensive L4 domain
knowledge (updatable via standard pipeline) while protecting frozen tiers (L1–L2).

**Status:** 🔶 Structurally resolved. Threshold values remain provisional (OQ-W1 — GAP-1
formally deferred to implementation phase).

---

## Summary Table

| Tension | Specialists | Status | Primary Resolution | Remaining Gap |
|---------|-------------|--------|--------------------|---------------|
| T1 — `attention_weight` authority | Graph Data Architect vs. MEMIT | ✅ Resolved | Two-number model (declared_importance + engine weight) | None |
| T2 — TGA independence vs. depth | Validation vs. Orchestration | ✅ Resolved | Four-layer TGA cascade | None |
| T3 — Meta-* audit vs. corpus integrity | Warden vs. Validation | 🔶 Partial | Sealed Corpus + per-case audit | OQ-V5 (corpus authorship policy) |
| T4 — Config authority fragmentation | Warden vs. State Consistency vs. Orchestration | ✅ Resolved | Three-tier `.harness/` model | None (v2: pre-receive hooks) |
| T5 — Token revocation vs. continuity | Warden vs. Orchestration | 🔶 Partial | Agent suspension + governance-state binding + D87 (OQ-S4 closed) | GAP-25 through GAP-28 (D87 residuals) |
| T6 — Genesis completeness vs. forgetting | Graph Data Architect vs. MEMIT | 🔶 Partial | Drift-from-anchor + capacity model + scope test | OQ-W1 (thresholds provisional — GAP-1 deferred) |
| T7 — Schema migration token timing | Warden vs. State Consistency | ✅ Resolved | Admission-time TTL; D85 closes OQ-TPC1 | GAP-23 (Genesis Hold lifecycle residual) |
| T8 — Write lock semantics conflation | State Consistency vs. Orchestration | ✅ Resolved | Lock / Hold split | OQ-CW1 (v2: voluntary release) |
| T9 — Compaction correctness vs. efficiency | MEMIT vs. Validation | 🔶 Partial | Full MEMIT re-run mandated; epoch bundling | OQ-OC3 (sample size protocol) |
| T10 — Out-of-band Git handling | State Consistency vs. Warden | ✅ Resolved | Two-queue model; no auto-compile | None (thresholds heuristic) |
| T11 — Audit trail vs. State Ledger | Warden vs. State Consistency | 🔶 Partial | Unified Ledger; sync/async split | OQ-SL1 (retention policy) |
| T12 — Unlocatable | Unknown | ⚠️ Unlocatable | Not traceable in spec body | Identification required — next full council session |
| T13 — Advisory boundedness vs. operational flexibility | MEMIT vs. Orchestration | 🔴 Open | — | Gap session required; blocks GAP-3 spec block 2c |
| T14 — Single-key vs. dual-key for ceremony authorization | Warden vs. Orchestration | 🔴 Open | — | Gap session required; blocks GAP-26, D90 planning |
| Pre-T1 — Immutability vs. mutability | Warden vs. State Consistency | ✅ Resolved (via T5, T11) | Mutability lifecycle per tier | T14 is adjacent (governance ceremony authorization) |
| Pre-T2 — Write volume vs. locality | Graph Data Architect vs. MEMIT | 🔶 Partial (via T6) | Capacity model + drift anchoring | OQ-W1 — GAP-1 formally deferred |
| Pre-T3 — Validator independence vs. scale | Validation vs. Orchestration | ✅ Resolved (via T2) | Four-layer cascade + scope-bounded dual-TGA | None |
| Pre-T4 — Audit completeness vs. throughput | Warden vs. State Consistency + MEMIT | 🔶 Partial (via T11) | Sync/async Ledger split | WAL cadence heuristic (GAP-14) |
| Pre-T5 — Schema stability vs. autonomy | Graph Data Architect vs. Orchestration | ⚠️ Partial (via T4) | Gate scope enforcement; extension protocol unspecced | Schema extension pathway (sub-gap in GAP-3) |
| Pre-T6 — Genesis completeness vs. lock-in | Graph Data Architect vs. MEMIT | 🔶 Partial (via T6) | Scope test + four-tier structure | OQ-W1 — GAP-1 formally deferred |

---

## Open Tensions Requiring Gap Sessions

| Tension | Required Specialists | Recommended Session | Blocks |
|---------|---------------------|---------------------|--------|
| T13 | MEMIT Specialist + Orchestration Comparativist | GS7 (after ceremony model resolved) | GAP-3 block 2c; Phase 2 exit |
| T14 | Warden + Orchestration Comparativist | GS4 (combine with GAP-26) | GAP-26; D90 planning; unified ceremony model |
| T12 | Unknown — identification required | Next full council session | Spec completeness |

---

*Tension Map v2.0 — 14 working-session tensions (T1–T14) + 6 pre-mapped tensions (Pre-T1 through Pre-T6)*
*Supersedes tension-map-v1.md*
*Two new open tensions (T13, T14) added from Gap Session 1 and Gap Session 3 respectively*
*Two tension updates: T5 (OQ-S4 closed by D87), T7 (OQ-TPC1 closed by D85)*
