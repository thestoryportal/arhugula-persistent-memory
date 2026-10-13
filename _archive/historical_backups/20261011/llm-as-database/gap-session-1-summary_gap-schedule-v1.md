# Gap Session 1 — `.larql` Schema Versioning v2 Outline

```
Session: Gap Session 1 of 8 — GAP-3 residuals
Primary skill: MEMIT Specialist
Secondary: Graph Data Architect (schema-version concern crosses the write/schema boundary)
Spec basis: v1.1 integrated spec (active baseline)
Scope: Verify v1.1 closure of GAP-3; produce v2 outline for OQ-W6 residuals
Status: Draft
Delivers to: gap-backlog-v[next], v2 planning kickoff
```

---

## 1. Purpose and Scope

This session targets the three residual items under OQ-W6 that v1.1 explicitly deferred to v2 (§18.3, §6):

- Migration manifest **authorship** ceremony.
- Version **deprecation** ceremony and notice period policy.
- Multi-version team deployment **advisory window** policy.

The session produces:
1. A verification verdict on the v1.1 closure of GAP-3 (§2).
2. Three v2 outline spec blocks — one per residual item (§3).
3. A position on whether `LARQL_VERSION_LEGACY` advisory is sufficient for the v1→v2 transition (§4).
4. Newly surfaced gaps and tensions (§5).
5. Gap Session Summary Block (§6).

Non-goals: no implementation language, no orchestration selection, no resolution of OQs outside the GAP-3 residual scope.

---

## 2. v1.1 Closure Verification

### 2.1 Chain integrity

The v1.1 chain for cross-version `.larql` patch handling is:

```
.larql patch (larql_syntax_version header, D81)
      │
      ▼
Gate pre-check #8 (§10.2, C-GATE-1)
      │  ├─ VERSION_REJECTED        (below min — hard, no retry budget)
      │  ├─ VERSION_UNSUPPORTED     (above current — hard, operator alert)
      │  └─ LARQL_VERSION_LEGACY    (between min and current — advisory, proceed)
      ▼
Gate produces migration_context (IC-MANIFEST)
      │  { source_version, target_version, manifest_ref, manifest_hash, ... }
      ▼
MEMIT Write Engine (verifies manifest_hash)
      │  Hash mismatch → MIGRATION_MANIFEST_TAMPERED (SECURITY, sync)
      ▼
Versioned patch parser (D82) applies manifest translation
      │  Translation failure → compaction aborts (D82)
      ▼
MEMIT compile → .vindex overlay
```

This chain is **runtime-complete**: every version state a patch can be in at arrival has a defined handler and a defined ledger outcome. IC-MANIFEST closes the Gate → MEMIT handoff. The versioned parser is the single point of translation. The manifest is Tier 1 config and hash-bound.

### 2.2 Seams identified

Three seams exist in the chain that the residual items either partially name or do not name at all.

**Seam 1 — Manifest authorship and update atomicity.**
The `larql_migration_manifest` is Tier 1 config. v1.1 requires that it be updated "at the same time as `current_larql_version` whenever a `.larql` syntax version advance occurs" (§8.10). This is a declarative requirement, not an enforced atomicity property. No mechanism prevents `current_larql_version` from advancing in isolation, leaving the manifest behind. A desynchronized update is a silent compile-time break — compaction succeeds on patches authored at the new version and fails on every patch authored at prior versions, even though they were valid at commit time.

This seam is the subject of v2 outline block §3.1.

**Seam 2 — Manifest completeness is not probed. (NEW GAP — not in OQ-W6 residual.)**
Nothing in the v1.1 spec verifies that the manifest covers every version pair in the active range `[min_supported_larql_version, current_larql_version]`. A missing edge in the version lattice (e.g., 1.1→1.2 absent when min=1.0 and current=1.3) surfaces only at compaction time as a translation failure for that specific pair. The Gate accepts patches at all versions between min and current via the advisory path, so Gate-time enforcement cannot catch the gap. This is a class of silent Tier 1 config misconfiguration that the spec currently has no probe for.

Surfaced as **GAP-[next]** in §5.

**Seam 3 — First-deprecation ceremony is unscheduled.**
v1.1 allows `larql_syntax_version: "1.0"` via `LARQL_VERSION_LEGACY` but does not define when or how 1.0 is ever moved below `min_supported_larql_version`. The advisory path has no forcing function, so in the absence of an explicit deprecation event, 1.0 remains advisory-acceptable forever. This collapses the versioning scheme's value proposition — versioning exists so old forms can be retired; without a retirement ceremony, the cost of every historical version is carried by the write layer indefinitely.

This seam is the subject of v2 outline block §3.2, with reinforcement from §3.3 (advisory window bounds).

### 2.3 Verdict

v1.1 closure of GAP-3 is **runtime-complete but lifecycle-incomplete**. The patch-arrival path is sealed; the config-lifecycle path (authorship, completeness, deprecation) is the residual surface area.

---

## 3. v2 Outline Spec Blocks

All IDs below are **provisional pending v2 ratification**. The blocks are outline-level — sufficient to scope v2 work, not sufficient to ratify as final spec.

---

### 3.1 Migration Manifest Authorship Ceremony — Spec Block (Provisional D83)

**Specialist provenance:** MEMIT Specialist (primary), AISecOps Specialist (secondary — trust boundary), Graph Data Architect (secondary — schema evolution).

**What it must do:**
- Define who is authorized to propose, sign, and commit changes to the `larql_migration_manifest`.
- Bind every manifest change to an atomic, same-transaction update of `current_larql_version` and related Tier 1 fields.
- Require test coverage of every new version-pair translation before the manifest change is accepted.
- Produce a signed, ledger-visible event on every manifest change.

**Hard constraints:**
- Manifest changes MUST be co-signed by two distinct authorized roles: a **schema-owner** role (ontology / `.larql` syntax authority) and a **Warden** role (trust-boundary authority). Single-signature manifest writes MUST be rejected at the Tier 1 config ingress.
- Manifest changes MUST be atomic with the corresponding `current_larql_version` advance. Partial updates — version advances without manifest, or manifest changes without version advance — MUST be rejected pre-commit.
- Manifest changes MUST be accompanied by **forward-translation tests** for every version pair they introduce, and **round-trip tests** where round-trip is defined by the schema-owner. Coverage shortfall MUST block commit.
- Manifest changes MUST emit a `MIGRATION_MANIFEST_UPDATED` ledger entry (sync, new type). Entry MUST carry: prior manifest hash, new manifest hash, `current_larql_version` before/after, test coverage report reference, both signing role identities.
- Manifest content MUST be hashed into the `genesis-seal.json` reference set so Warden can detect offline tampering.

**Tradeoffs decided (outline — full v2 decision deferred):**
- **Option A — Warden sole signer.** Tight security, poor ergonomics for schema evolution, single point of unavailability.
- **Option B — Schema owner proposes, Warden ratifies (dual-role).** Standard zero-trust two-signature pattern. Recommended.
- **Option C — M-of-N key quorum on Tier 1 commits.** Highest security, heaviest operational burden, likely overscoped for v2.

Option B is the recommended v2 direction, pending ratification against the Warden's trust-boundary preferences in a later gap session.

**Open questions (deferred):**
- Should the manifest include a declared minimum test coverage field that the Gate cross-references at handoff time? (Secondary defense against a Tier 1 commit that passed signing but skipped tests.)
- Is there a "frozen manifest" state for fully-retired versions, in which no further edits are allowed even with dual signatures? (Prevents late rewrites of historical translations.)
- Key rotation cadence for schema-owner and Warden roles — owned by Warden domain, not this block.

**Interface contract (outline):**

```
IC-MANIFEST-SIGN (provisional) — Tier 1 Config ingress → Manifest Store
  From: Tier 1 Config ingress authority
  To:   Manifest Store (component holding larql_migration_manifest canonical copy)
  What A exposes: Signed manifest update envelope:
    { proposed_manifest_hash, prior_manifest_hash,
      current_larql_version_before, current_larql_version_after,
      schema_owner_signature, warden_signature,
      test_coverage_manifest_ref, test_coverage_hash,
      atomic_bundle_id  // binds manifest change to version advance }
  Conditions: Ingress MUST verify both signatures against Tier 1 role registry before
    admitting the envelope. Atomic bundle MUST contain both manifest change and version
    advance records; partial bundles MUST be rejected. Test coverage manifest MUST include
    every new version pair introduced by this update.
  Failure behavior: Signature failure, atomicity failure, or coverage shortfall → envelope
    rejected; MIGRATION_MANIFEST_UPDATE_REJECTED ledger entry (sync) with failure reason;
    Warden notified for signature or coverage failures.
```

**Non-goals:**
- Does not specify the role registry mechanism — that is a Warden-domain artifact.
- Does not specify the test harness implementation — spec remains implementation-agnostic.
- Does not authorize emergency override ("break-glass" single-signature path). Any such path requires its own spec block and is not included in this outline.

---

### 3.2 Version Deprecation Ceremony and Notice Period Policy — Spec Block (Provisional D84)

**Specialist provenance:** MEMIT Specialist (primary), State Consistency Theorist (secondary — compaction/drainage timing), Graph Data Architect (secondary — schema lifecycle).

**What it must do:**
- Define the notice period between deprecation announcement and `min_supported_larql_version` advancing past a given version.
- Define what operators and Coder Agents MUST do during the notice window.
- Define the state of the ledger, the archive, and the advisory path for the deprecated version at every phase of the ceremony.
- Coordinate deprecation timing with the compaction cadence so active patches authored under the deprecated version reach a safe state before the hard cutoff.

**Hard constraints:**
- A version MUST NOT be removed from `min_supported_larql_version` (i.e., advanced past) while any **active, non-superseded** `.larql` patch exists authored under that version. Drainage precedes cutoff.
- A deprecation event MUST be announced via a `VERSION_DEPRECATION_SCHEDULED` ledger entry (sync, new type) containing: deprecated version, scheduled cutoff date or cutoff condition, notice period basis, at-scheduling-time active patch count at that version.
- Once deprecation is scheduled but before cutoff, the Gate MUST continue to accept patches at the deprecated version under the advisory path, **but MUST additionally emit a `VERSION_DEPRECATION_WARNING` entry per patch** to signal active authorship at a version that is being retired.
- At cutoff, Gate pre-check #8 MUST reclassify the deprecated version from `LARQL_VERSION_LEGACY` (advisory) to `VERSION_REJECTED` (hard). Reclassification MUST be atomic with `min_supported_larql_version` advance and MUST emit `VERSION_DEPRECATED` (sync).
- Superseded patches in the archive at the deprecated version remain valid for compaction re-parse as long as the migration manifest covers the deprecated→current translation path. Manifest entries for deprecated versions MUST NOT be removed from the manifest; deprecation removes the version from acceptable-authorship, not from translatable-history.

**Tradeoffs decided (outline — full v2 decision deferred):**
- **Option A — Calendar-based notice (e.g., 30 days).** Predictable, independent of system load, operator-friendly. Risk: calendar expires while active patches remain; forces either cutoff-with-abandonment or cutoff-postponement, both bad.
- **Option B — Compaction-cycle-based notice (one full cycle after announcement).** Tied to actual patch drainage behavior, respects system rhythm. Risk: compaction cadence variability leaks into deprecation timing.
- **Option C — Drainage-based (wait until zero active patches at deprecated version).** Safest. Risk: a stuck or orphaned patch blocks deprecation indefinitely.
- **Option D — Hybrid: announce with a target cutoff condition (drainage OR compaction-cycle-count OR calendar, whichever later), with operator-triggered drainage sweep.** Recommended outline.

Option D is the recommended direction. The recommended cutoff condition is: *deprecation cutoff occurs when `(active_patch_count_at_deprecated_version == 0) OR (N compaction cycles elapsed, default 2) OR (M calendar days elapsed, default 90)`, whichever is later, with an operator-authorized forced-cutoff path for the stuck-patch case.*

All threshold values (N, M) are **provisional pending empirical validation against target deployment velocity**.

**Open questions (deferred):**
- What happens if a Coder Agent is offline during the notice window and returns after cutoff with a queued patch at the now-deprecated version? Quarantine path vs. re-authorship-required vs. deprecated-patch-archive.
- Does a scheduled deprecation trigger **forced compaction** to accelerate drainage, or only notification?
- What is the minimum notice period below which deprecation is never allowed (floor), independent of drainage status? (Prevents same-day surprise deprecation.)
- Rollback path: if a deprecation is announced and then withdrawn before cutoff, what is the ledger representation? Can a version be "un-deprecated"?

**Interface contract (outline):**

```
IC-DEPRECATION-SCHED (provisional) — Orchestrator ↔ Gate
  From: Orchestrator (authority on deprecation schedule)
  To:   Gate (pre-check #8)
  What A exposes: Current deprecation schedule view:
    { scheduled: [{ version, cutoff_condition, cutoff_state, announce_ledger_ref }],
      current_larql_version, min_supported_larql_version }
  Conditions: Gate MUST consult schedule on every pre-check #8 evaluation. Gate MUST
    emit VERSION_DEPRECATION_WARNING (async) for each patch at a version that is
    scheduled but not yet cut off. Gate MUST NOT advance min_supported_larql_version
    by its own action — only by atomic commit from Orchestrator.
  Failure behavior: Schedule view unavailable → Gate treats as "no deprecations scheduled"
    (fail-open for deprecation awareness, fail-safe for rejection — patches still pre-checked
    against current min). Schedule-inconsistent-with-config → GATE_SCHEDULE_MISMATCH
    (SECURITY, sync); Warden notified.
```

**Non-goals:**
- Does not specify how operators are notified out-of-band (email, dashboard, pager) — that is an operational concern.
- Does not specify the minimum viable deprecated-version set — any version between min and current is deprecable under this ceremony.
- Does not prescribe compaction cadence itself — compaction cadence is owned by State Consistency domain.

---

### 3.3 Multi-Version Team Advisory Window Policy — Spec Block (Provisional D85)

**Specialist provenance:** MEMIT Specialist (primary), Orchestration Comparativist (secondary — multi-agent coordination), AISecOps Specialist (secondary — replay attack surface).

**What it must do:**
- Define the bounded window during which `LARQL_VERSION_LEGACY` advisory is acceptable for a given deprecated-but-not-cutoff version.
- Define the forcing function that escalates advisory into hard rejection before the formal deprecation cutoff when the system observes excessive legacy drift.
- Define the operational signal that tells operators: your Coder Agent team has split-version drift; align.
- Prevent the advisory path from becoming a permanent fallback for agents that refuse or fail to migrate.

**Hard constraints:**
- Every `LARQL_VERSION_LEGACY` advisory emission MUST increment a per-version `legacy_advisory_count` counter held by the Orchestrator and reflected in the Ledger.
- The Orchestrator MUST enforce an **advisory window cap** per deprecated-but-not-cutoff version. The cap is hybrid: `min(calendar_window, legacy_patch_count_window)`. Hitting either bound triggers early promotion to hard rejection for new patches at that version, independent of the formal deprecation cutoff. Active patches already committed under the advisory remain valid.
- Cap breach MUST emit a `LARQL_VERSION_ADVISORY_CAP_BREACHED` ledger entry (sync, new type) with the breached bound, the per-version counter state, and the identities of Coder Agents whose patches last incremented the counter.
- Advisory state MUST be exposed to the operator dashboard via a standard ledger query — the system MUST NOT require out-of-band observability to know it is in advisory mode.
- The advisory window counter MUST reset only on: (a) formal deprecation cutoff (the version leaves advisory-acceptable entirely), or (b) all active patches at that version being superseded. A Coder Agent identity change does NOT reset the counter.

**Tradeoffs decided (outline — full v2 decision deferred):**
- **Option A — Time-bounded (calendar-only).** Simple. Predictable. Risk: a burst of legacy authorship consumes the bound quickly with no per-volume sensitivity.
- **Option B — Volume-bounded (N legacy patches only).** Tied to actual usage. Risk: variable calendar; a slow team stays in advisory indefinitely.
- **Option C — No bound (advisory valid until deprecation cutoff).** Simplest. Directly the flaw being addressed — version sprawl, no forcing function.
- **Option D — Hybrid: `min(calendar_window, legacy_patch_count_window)`.** Tightest safety, operator ergonomics acceptable.

Option D is the recommended direction. Both bounds are **provisional pending empirical validation**. Suggested starting provisional values: calendar window = 30 days from version activation as `LARQL_VERSION_LEGACY`; patch count window = 100 legacy-advisory emissions at that version.

**Open questions (deferred):**
- Should the advisory counter be per Coder Agent identity or strictly global? The hard constraint above selects global — revisit if empirical use exposes false-positive cap breaches caused by a single runaway agent.
- Does a newly onboarded Coder Agent get a fresh advisory budget at a given legacy version, or does the global counter cover it? (The hard constraint above selects global.)
- How does the advisory window interact with the Pruning Agent? Should patches emitted under advisory be preferentially pruned, or marked for preferential supersession at next compaction?
- If the cap is breached mid-session by a single batch of patches, is there a batch-rejection path or only forward-going rejection?

**Interface contract (outline):**

```
IC-ADVISORY-CAP (provisional) — Orchestrator ↔ Gate
  From: Orchestrator (authority on advisory counters)
  To:   Gate (pre-check #8 extension)
  What A exposes: Per-version advisory cap status:
    { [version]: { legacy_advisory_count, calendar_window_elapsed_fraction,
                   patch_count_window_elapsed_fraction,
                   cap_state: NOMINAL | APPROACHING | BREACHED } }
  Conditions: Gate MUST check cap_state on every pre-check #8 LARQL_VERSION_LEGACY
    decision. BREACHED versions MUST be treated as VERSION_REJECTED for new patches
    (hard rejection, no retry budget) even if the formal deprecation cutoff has not
    occurred. APPROACHING state MUST surface in the Gate's advisory ledger entry.
  Failure behavior: Counter unavailable → Gate treats all legacy versions as NOMINAL
    (fail-open for safety-reject is too punitive for unknown counter state); emits
    ADVISORY_COUNTER_UNAVAILABLE (SECURITY-adjacent, sync); Warden notified.
```

**Non-goals:**
- Does not specify the Coder Agent identity system — that is an Orchestration / Warden domain artifact.
- Does not specify the operator-facing dashboard visualization — spec-level requirement is only that the state be queryable via standard ledger mechanisms.
- Does not itself deprecate any specific version; this block defines the advisory window mechanic, deprecation scheduling lives in §3.2.

---

## 4. Advisory Path Sufficiency for v1→v2 Transition

The specific question: is `LARQL_VERSION_LEGACY` advisory sufficient for the v1→v2 transition, or does the spec need a harder transition timeline?

**Position:** The advisory path is *sufficient as the transition mechanism* and *insufficient as the transition policy*. These are different claims.

The **mechanism** is correct because:
- It preserves service continuity — existing Coder Agents authored under `larql_syntax_version: "1.0"` continue to commit successfully during the transition.
- The Gate still enforces every other pre-check, so version compatibility does not smuggle in other validity relaxations.
- The migration manifest translates 1.0 → 1.1 at compile time, keeping the overlay file semantics aligned with the current version regardless of the authored version.

The **policy** is insufficient because:
- Without a scheduled cutoff for 1.0 and without an advisory cap, the "transition" has no endpoint. The system can run indefinitely with a mix of 1.0 and 1.1 patches, carrying the operational weight of two syntax versions forever.
- An attacker in possession of an old 1.0 `.larql` patch could, in principle, replay it into the system through the advisory path at any future date. Every additional day of open advisory is an additional day of replay-attack surface against an older, possibly weaker validity contract. The Warden's position on this is not trivially captured by the advisory path alone.
- A multi-version team with no forcing function has no operational pressure to align on a single version. This is the multi-agent coordination failure mode the residual item (c) is about.

**Recommendation for v2 planning kickoff:**
1. On the first invocation of a `larql_syntax_version` advance (1.0 → 1.1 in practice), **schedule the deprecation of 1.0 concurrently with the advance**. Use the §3.2 ceremony. Provisional notice window: `min(90 days, 2 compaction cycles)` — whichever later.
2. In parallel, set the §3.3 advisory cap for 1.0. Provisional cap: 100 legacy-advisory emissions OR 30 days of advisory tenure, whichever first.
3. The two mechanisms are complementary. The advisory cap catches fast-drift scenarios (many Coder Agents stuck on 1.0 authoring rapidly). The formal deprecation ceremony catches slow-drift scenarios (low authoring rate but persistent legacy tail). Together they bound the transition.

This recommendation is **outline-level** and requires ratification by the Warden (for replay-attack-surface budget) and the State Consistency Theorist (for compaction-cycle-count selection) before entering v2 spec proper.

---

## 5. Newly Surfaced Items

### 5.1 New gap surfaced during verification

**GAP-[next, to be assigned in gap-backlog-v[next]]**
**Domain(s):** MEMIT Specialist (primary), AISecOps Specialist (secondary)
**Description:** The v1.1 spec does not require the `larql_migration_manifest` to cover every version pair in `[min_supported_larql_version, current_larql_version]`. A gap in the version lattice surfaces only at compaction time as a translation failure. No pre-commit probe verifies lattice completeness.
**Blocked by:** v2 spec block §3.1 ratification (manifest authorship ceremony — natural home for a completeness check).
**Blocks:** Full v2 closure of `.larql` schema versioning.
**Priority:** High (silent Tier 1 config error class; discoverable today).

### 5.2 New tensions surfaced

**TENSION-13 (provisional): MEMIT Specialist vs. AISecOps Specialist — Manifest signing ownership**
**Status:** Surfaced, unresolved.
**Framing:** The `larql_migration_manifest` is a schema artifact (what MEMIT Specialist and Graph Data Architect own) that is simultaneously a trust-boundary artifact (what the Warden owns). The authorship ceremony (§3.1) proposes dual signatures, but does not resolve which domain is the **canonical owner** of manifest content authorship vs. signing authority. A lopsided resolution — Warden-owned content, or schema-owner-owned trust — is worse than an explicit split.
**Proposed resolution direction:** Schema owner is the canonical **content author** (proposes manifest entries); Warden is the canonical **signing authority** (ratifies the cryptographic attestation). Commit to this as T13 resolution in a later gap session.

**TENSION-14 (provisional): MEMIT Specialist vs. State Consistency Theorist — Deprecation timing vs. compaction cadence**
**Status:** Surfaced, unresolved.
**Framing:** Deprecation cutoff depends on drainage of active patches at the deprecated version (§3.2 hard constraint). Drainage is driven primarily by compaction cycles. Compaction cadence is owned by State Consistency. If the two domains select independent cadences — deprecation cutoffs scheduled on calendar, compaction scheduled on drift thresholds — the drainage-before-cutoff invariant can be violated silently. A shared cadence anchor is needed.
**Proposed resolution direction:** Deprecation cutoff condition expressed in compaction-cycle units rather than calendar units wherever possible; State Consistency Theorist owns the cycle definition; MEMIT Specialist consumes it. Commit to this as T14 resolution in a later gap session.

---

## 6. Gap Session Summary Block

```
═══════════════════════════════════════════════════════════════════════════════
  GAP SESSION 1 — SUMMARY BLOCK
  Topic: .larql schema versioning — v1.1 closure verification + v2 outline
  Primary skill: MEMIT Specialist
  Secondary: Graph Data Architect, AISecOps Specialist, State Consistency Theorist
  Target OQ: OQ-W6 (residual — three sub-items per §18.3)
═══════════════════════════════════════════════════════════════════════════════

GAPS RESOLVED:
  (none fully resolved — this session produces v2 outline, not v2 ratification)

GAPS PARTIALLY RESOLVED:
  • GAP-3 (OQ-W6 residual)
      Partial: Runtime chain (Gate → migration_context → MEMIT → versioned parser →
        compaction re-run) is verified runtime-complete in v1.1. Lifecycle chain
        (authorship, deprecation, advisory window) is scoped into three v2 outline
        spec blocks (provisional D83, D84, D85) with hard constraints, tradeoff
        frames, proposed interface contracts (IC-MANIFEST-SIGN, IC-DEPRECATION-SCHED,
        IC-ADVISORY-CAP), and open questions.
      Remains open: v2 ratification of the three outline blocks; threshold calibration
        for notice periods and advisory caps (all provisional pending empirical data);
        first-use scheduling of 1.0 deprecation; resolution of T13 and T14.

GAPS DEFERRED:
  (none newly deferred — all items either resolved-partial or escalated to new gap)

NEW GAPS SURFACED:
  • GAP-[next]: Migration manifest lattice completeness probe
      No pre-commit verification that larql_migration_manifest covers every version
      pair in [min_supported_larql_version, current_larql_version]. Today a missing
      lattice edge fails only at compaction time. Natural home for the probe: the
      §3.1 authorship ceremony (manifest update rejected if coverage is not lattice-
      complete). Priority: High.

NEW TENSIONS SURFACED:
  • T13 (provisional): MEMIT Specialist vs. AISecOps Specialist — manifest signing
      ownership. Proposed direction: schema owner authors content, Warden signs.
      Unresolved.
  • T14 (provisional): MEMIT Specialist vs. State Consistency Theorist — deprecation
      cutoff timing vs. compaction cadence. Proposed direction: deprecation cutoffs
      expressed in compaction-cycle units, cadence definition owned by State
      Consistency. Unresolved.

ADVISORY PATH SUFFICIENCY (v1→v2 transition):
  • LARQL_VERSION_LEGACY is sufficient as transition MECHANISM, insufficient as
    transition POLICY. v2 must pair the advisory path with (a) formal deprecation
    schedule for 1.0 concurrent with the 1.0→1.1 advance, and (b) bounded advisory
    cap per §3.3. Advisory without a forcing function is indefinite, which defeats
    the versioning scheme.

PROVISIONAL IDs ISSUED (require v2 ratification):
  • D83 — Migration Manifest Authorship Ceremony
  • D84 — Version Deprecation Ceremony and Notice Period Policy
  • D85 — Multi-Version Team Advisory Window Policy
  • IC-MANIFEST-SIGN — Tier 1 Config ingress → Manifest Store
  • IC-DEPRECATION-SCHED — Orchestrator ↔ Gate
  • IC-ADVISORY-CAP — Orchestrator ↔ Gate
  • New ledger entry types (sync): MIGRATION_MANIFEST_UPDATED,
    MIGRATION_MANIFEST_UPDATE_REJECTED, VERSION_DEPRECATION_SCHEDULED,
    VERSION_DEPRECATION_WARNING, VERSION_DEPRECATED,
    LARQL_VERSION_ADVISORY_CAP_BREACHED, ADVISORY_COUNTER_UNAVAILABLE

FEEDS INTO:
  • gap-backlog-v[next]: add surfaced manifest-lattice gap
  • tension-map-v[next]: add T13 and T14 with proposed resolution directions
  • v2 planning kickoff: three outline blocks (D83, D84, D85) become starting
    surface area for v2 spec proper
  • Future gap session involving Warden: resolve T13 (signing ownership)
  • Future gap session involving State Consistency: resolve T14 (cadence anchor),
    ratify compaction-cycle units for deprecation timing

═══════════════════════════════════════════════════════════════════════════════
```

---

## 7. Provenance and Non-Goals

**Specialist provenance:** MEMIT Specialist (primary); Graph Data Architect (secondary, schema versioning is a schema-lifecycle concern); AISecOps Specialist (secondary, manifest signing and replay-attack surface); State Consistency Theorist (secondary, deprecation-compaction timing interaction); Orchestration Comparativist (tertiary, multi-agent advisory coordination).

**What this session does not do:**
- Does not ratify D83, D84, or D85 — all three are v2 outline only.
- Does not select between Option A/B/C/D tradeoffs — recommendations are surfaced; final selection belongs to v2 spec proper.
- Does not specify implementation language, orchestration framework, cryptographic primitives, or key management mechanism.
- Does not resolve T13 or T14 — they are surfaced for later cross-domain gap sessions.
- Does not assign final numeric values to any provisional threshold (notice period, advisory window, cap, compaction cycle count) — all require empirical calibration against target deployment.
- Does not authorize an emergency break-glass override path for any of the three ceremonies.
