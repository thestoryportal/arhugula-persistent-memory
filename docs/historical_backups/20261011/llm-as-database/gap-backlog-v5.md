# LLM as Database: Agent Harness Architecture
## Gap Backlog v5.0

> **Supersedes:** `gap-backlog-v4.md`
> **Source sessions:** GS10, GS11, GS12 summaries
> **Delta basis:** gap-backlog-v4.md (54 gaps) + 6 new gaps from GS10–11 + status updates
> **Total gaps tracked:** 60 — includes all v4 gaps updated with GS10–12 closure status
> **Active tensions requiring sessions:** T16, T-S4-N2 (via GAP-40 closed), T-BT
> **Resolved in GS10–12:** T-SC-W-2, T-S4-N1, T-S7-N1, T-PM-vs-PA, T-TGA-load
> **New tensions (GS10):** T-W-BG-1 (accepted), T-S-RP-1 (accepted for v1)

---

## ⚠️ Numbering Note (v4 → v5)

GS10 session summary labeled its new gaps GAP-48 through GAP-51. These collide with
backlog-v4 canonical GAP-48 through GAP-54 (from v2 reconciliation). Resolution: GS10
and GS11 new gaps are assigned canonical IDs GAP-55 through GAP-60 in this document.
GS10 session summary references to GAP-48/49/50/51 map as follows:

| Session label | Canonical (v5) |
|---|---|
| GS10 "GAP-48" | GAP-55 |
| GS10 "GAP-49" | GAP-56 |
| GS10 "GAP-50" | GAP-57 |
| GS10 "GAP-51" | GAP-58 |
| GS11 "GAP-55" | GAP-59 |
| GS11 "GAP-56" | GAP-60 |

---

## Status Labels

| Status | Meaning |
|--------|---------|
| ✅ **Resolved** | Fully closed |
| 🔶 **Partial** | Partially closed; residuals remain |
| 🔴 **Open** | Not yet addressed |
| ⏳ **Deferred** | Formally deferred with rationale |
| 🔜 **Pending GS13** | Scope confirmed for final council session |
| 🔒 **Accepted** | Accepted as deployment-specific or design constraint |

---

## Carry-Forward from v4 — Updated Status Only

*(Full gap descriptions remain in gap-backlog-v4.md. Only status changes listed here.)*

### Resolved in GS10

| GAP | Previous Status | Resolution (GS10) |
|-----|----------------|-------------------|
| GAP-29 (a+b) | 🔴 Open | ✅ Resolved. (a) IC-MANIFEST-1 Check 8 added; `MANIFEST_LATTICE_INCOMPLETE` (SECURITY, sync). (b) W3 scope consolidation policy; C-W3-1 admission criteria; IC-W3-POLICY-1. |
| GAP-33 | ✅ Resolved (v2 GS8 — verify only) | ✅ Confirmed consistent with CeremonyToken framework + `.dry-run-store/` spec added: `<harness_root>/.dry-run-store/`, 37-day min retention, operator-owned, Warden metadata-only audit. IC-DRS-1. |
| GAP-36 | 🔴 Open | ✅ Resolved. N=5 / M=60min, advisory + operator alert (observability model, not enforcement). IC-CRR-1. |
| GAP-37 | 🔴 Open | ✅ Resolved. §11.8.1 governance write carve-out text ratified with W3 cross-reference. **T-SC-W-2 CLOSED.** IC-GCO-1. |
| GAP-40 | 🔴 Open | ✅ Resolved. Dual-root signing model (operator root + harness release key); atomic write; signed boot manifest; refuse-boot on verification failure. C-BOOT-5: `operator_root_public_key` compile-time-embedded. IC-BOOT-1. |
| GAP-41 | 🔴 Open | ✅ Resolved. N=5 / 10min burst limit per CAK; `BURST_SUSPENDED` state on breach; 60-min auto-clear or Tier 1 explicit clear. IC-CAKB-1. |
| GAP-42 | 🔴 Open | ✅ Resolved. Break-glass: second Tier 1 anchor, M≥3 of N quorum, physical-access injection, `CAK_ROTATION_EMERGENCY` ceremony, `TRUST_ROOT_LOST` terminal double-compromise state. **Closes OQ-S-CAK-1.** IC-BG-1. |
| GAP-44 | 🔴 Open | ✅ Resolved. `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` INTEGRITY baseline + `GENESIS_INITIATION_ABUSE_PATTERN` SECURITY aggregate (≥3 in 60min). Neither W3-eligible per C-W3-1. IC-GIB-1. |
| GAP-47 | 🔴 Open | ✅ Resolved. `RETENTION_PRUNING` ceremony type added; `artifact_retention_manager` role. IC-RP-1. |

### Resolved in GS11

| GAP | Previous Status | Resolution (GS11) |
|-----|----------------|-------------------|
| GAP-30 | 🔴 Open | ✅ Resolved. Paired sync-write constraint C-GTO-1; monitor pairing-check C-GTO-2 on full verification; `GENESIS_TIMEOUT_TRIP_MISSING` (CONSISTENCY, async, W1). IC-MON-GTOTM. |
| GAP-31 | 🔴 Open | ✅ Resolved. C-GEN-REC-3 enforcement: operator-cited precursor, Ledger lookup, Hold coverage + audit-window checks. `HOLD_RELEASE_REASON_UNWARRANTED` (SECURITY, sync, W1 — not W3 per C-W3-1). IC-REL-PRECURSOR, IC-TC-PRECURSOR-QUERY. |
| GAP-34 | 🔴 Open | ✅ Resolved. R-S3-3 applied: `governing_scope_hash` added to PREPARED and COMMITTED entries; captured at PREPARE, preserved at COMMIT, nullable for pre-amendment entries. IC-PREPARE-SCOPE. |
| GAP-35 | 🔴 Open | ✅ Resolved. Option (a) ratified: consumed tokens proceed to natural outcome. §11.8.1 one-sentence addition. |
| GAP-43 | 🔴 Open | ✅ Resolved. Standard IC-TC-RESET sufficient for BOUNDED_COMPENSATION_VIOLATION-triggered trips; forensic record is CIRCUIT_TRIPPED with trip_reason: TC_COMPENSATION_OVER_SCOPE. |
| GAP-46 | 🔴 Open | ✅ Resolved. Stable external `operator_id` bound at first-boot CAK registration, carried across rotation. **Closes T-S4-N1** (rotation registry ordering) and **T-S7-N1** (RATE_LIMIT_RETENTION_CONFLICT boot-time validation). IC-CAK-IDENTITY, IC-BOOT-RLRF. |
| GAP-52 | 🔴 Open | ✅ Resolved. D104 manifest amended: `signer_public_key_material` field added; `ARCHIVE_KEY_SEALED` Ledger entry at seal time; Genesis Seal cross-check at restore. No separate key-archive ceremony needed. |
| GAP-53 | 🔴 Open | ✅ Resolved. §16.4 documentation: 100K–1M typical project range; 10M infeasibility threshold on reference hardware. Sampled-verification flagged for v2 (GAP-59). |
| GAP-54 | 🔴 Open | ✅ Resolved. Option (b): hook binary hash in Tier 2 sealed `hook-registry/v1`; boot-time verification; `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) on mismatch. IC-HOOK-BOOT. |
| T-PM-vs-PA | 🔶 Partial | ✅ **Tension resolved.** Merge + CORE-tier priority elevation; single review queue item per `edge_id`; both-reason acknowledgment required. IC-REVIEW-QUEUE amended. |

### Resolved in GS12

| GAP | Previous Status | Resolution (GS12) |
|-----|----------------|-------------------|
| GAP-38 | 🔴 Open | ✅ Resolved. N=10, M=60s sliding window, per-Orchestrator-instance global scope. Dual alert path: `SCOPE_MISMATCH_AGGREGATE_ALERT` (SECURITY, async, W1) + review queue cross-link. Counter not reset on review; cooldown = M seconds. IC-AGG-COUNTER, IC-AGG-ALERT-LINK. |
| GAP-39 | 🔶 Partial | ✅ Resolved. `clock_stub_required` flag required on every constitutional test. Sandbox synthetic-clock injection mandatory when true. Missing injection → `SANDBOX_CONFIG_ERROR` (not test failure). Q5 evidence schema extended with two discriminated shapes. OQ-V9 resolved: nomination-time declarative attestation + dry-run is sufficient for v1.1. IC-CLK-META, IC-CLK-SANDBOX, IC-NOM-DRYRUN. |
| T-TGA-load | 🔴 Open | ✅ **Tension closed as 📋 Accepted for v1.** TGA verification-artifact concentration is governed by D32–D33 independence constraint, not an oversight. v2 reconsider flag set if v1.1 operation surfaces evidence for a TGA-Test / TGA-Probe split. |

### Status Unchanged in GS10–12 (remain open — GS13 scope)

| GAP | Status | GS13 Role |
|-----|--------|-----------|
| GAP-4 | 🔴 Open (externally blocked) | Contingent path specs (A/B/C) |
| GAP-9 | 🔶 Partial (v2 GS10 protocol) | Confirm status |
| GAP-13 | 🔴 Open | v2 outline |
| GAP-15 | ⏳ Deferred (GAP-1) | Confirm deferral |
| GAP-17 | ⏳ v2-deferred | v2 outline |
| GAP-18 | ⏳ v2-deferred | v2 outline |
| GAP-19 | ⏳ v2-deferred | v2 outline |
| GAP-27 | ✅ Resolved (conflict outstanding) | Resolve Tier 1 vs. Tier 3 placement |
| GAP-32 | ⏳ v2-deferred | v2 outline |
| GAP-48 | 🔴 Open | Probe set versioning for ε calibration |
| GAP-49 | 🔴 Open | Self-referential probing |
| GAP-50 | 🔶 Partial (T-TGA-load triage covers) | Confirm status |
| GAP-51 | 🔴 Open | Provenance record lifecycle |
| GAP-55 | 🔴 Open | New — see below |
| GAP-56 | 🔴 Open | New — see below (affects GAP-4 path specs) |
| GAP-57 | 🔴 Open | New — see below (affects GAP-4 path specs) |
| GAP-58 | 🔴 Open | New — see below (affects GAP-4 state machine) |

---

## New Gaps — GAP-55 Through GAP-60

---

### GAP-55
**Domain:** Warden + State Consistency Theorist | **Priority:** 🟢 Low | **Status:** 🔴 Open
**Source:** GS10 (session label "GAP-48")

Aggregate-detection entry type convention. GAP-44's `GENESIS_INITIATION_ABUSE_PATTERN` (aggregate-signal entry alongside individual entries) establishes a pattern that may recur. Whether aggregate-signal entries always carry: always SECURITY category; always contain a `source_entry_hash_list` field; always require cross-linked review queue item — is not formalized as a framework convention. **Candidate for GS13 or post-v1 integration pass.** Low-impact if deferred; creates inconsistency risk if future sessions add aggregate entries without knowing the convention.

---

### GAP-56
**Domain:** Warden + State Consistency Theorist | **Priority:** 🟡 Medium | **Status:** 🔜 Pending GS13
**Source:** GS10 (session label "GAP-49")

Genesis ceremony event-count modeling. GAP-41 established N=5 / 10min as the per-CAK burst limit. No empirical modeling of worst-case legitimate Genesis ceremony sequences has been performed. A project performing rapid Genesis recovery (e.g., multiple Genesis timeout-and-reset cycles in a debugging session) might exceed N=5 in 10 minutes legitimately. Before v1 ship, the worst-case legitimate sequence must be modeled to confirm the burst limit does not false-positive on real operator workflows. **GS13 relevance:** GAP-4 contingent path specs may specify Genesis-heavy workflows on specific paths — the burst limit assumption must be path-aware.

---

### GAP-57
**Domain:** Warden + Orchestration Comparativist | **Priority:** 🟡 Medium | **Status:** 🔜 Pending GS13
**Source:** GS10 (session label "GAP-50")

Per-operator harness binary implication. GAP-40 established C-BOOT-5: `operator_root_public_key` is embedded at compile time, making harness binaries non-universal artifacts — each operator requires their own build. Implications for release process, reproducible builds, and patch distribution are undefined. **Direct GS13 relevance:** GAP-4 contingent path specs must account for the fact that Path A (LangGraph), Path B (SDK), and Path C (Hybrid) may have different build/distribution assumptions. A path-conditional deployment architecture may be needed.

---

### GAP-58
**Domain:** State Consistency Theorist + Warden | **Priority:** 🟡 Medium | **Status:** 🔜 Pending GS13
**Source:** GS10 (session label "GAP-51")

New state lifecycle integration. GS10 introduced `BURST_SUSPENDED` (GAP-41) and `TRUST_ROOT_LOST` (GAP-42) as new harness states. Their interaction with the existing §11.8 state machine (CIRCUIT_TRIPPED → READ_ONLY → WRITE_ENABLED via IC-TC-RESET) is not explicitly modeled. Can a harness in `BURST_SUSPENDED` still process circuit resets? Can a harness in `TRUST_ROOT_LOST` do anything at all? **Direct GS13 relevance:** GAP-4 path specs reference the TC and orchestration control plane — the complete state machine must be defined before path-conditional behavior can be specced.

---

### GAP-59
**Domain:** State Consistency Theorist | **Priority:** 🟢 Low | **Status:** ⏳ v2-deferred
**Source:** GS11 (session label "GAP-55")

Sampled-verification design for Ledger chains exceeding 10M entries (GAP-53 documentation threshold). Coverage guarantee, sampling distribution, integration with C-GTO-2 pairing-check. Deferred to v2 per GAP-53. No GS13 action required.

---

### GAP-60
**Domain:** Warden | **Priority:** 🟢 Low | **Status:** ⏳ v2-deferred
**Source:** GS11 (session label "GAP-56")

Retired-key revocation metadata semantics. When a Ledger archive bundle's signing key has been retired, restoration must classify the retirement reason (retired-clean vs. retired-compromised) because the trust implication differs — a compromised retired key creates a different restoration risk profile. Deferred to v2 per GAP-52 open question. No GS13 action required.

---

## GS13 Scope — Updated

**Carry-forward items (unchanged from v4 GS13 plan):**
- GAP-4: Three contingent path specs (Path A/B/C)
- GAP-9: Confirm partial resolution status (v2 GS10 probe protocol)
- GAP-13: v2 outline (Genesis automation proxy)
- GAP-15: Formal deferral confirmation
- GAP-17, GAP-18, GAP-19, GAP-32: v2 outlines
- GAP-27: Resolve Tier 1 vs. Tier 3 placement for `scope_update_min_interval_seconds`
- GAP-48: Probe set versioning for ε calibration (MEMIT)
- GAP-49: Self-referential probing (Validation + MEMIT)
- GAP-50: Confirm status via T-TGA-load triage (Validation)
- GAP-51: Provenance record lifecycle (SCT + MEMIT)
- T15: v2 resolution path + A11
- OQ-SC3: Stale Layer 4 fact reconciliation workflow

**New additions from GS10–11 that must be in GS13:**
- GAP-55: Aggregate-detection entry type convention (Low — quick decision)
- GAP-56: Genesis ceremony event-count modeling (Medium — affects GAP-4 burst-limit assumptions)
- GAP-57: Per-operator harness binary implication (Medium — affects GAP-4 path deployment specs)
- GAP-58: New state lifecycle integration (Medium — affects GAP-4 state machine completeness)

**GS13 session length:** Now **Long** (was Medium in v4). GAP-56/57/58 all touch GAP-4 directly.

---

## Phase 2 Exit Criteria — Post GS10–12

| Criterion | Status |
|-----------|--------|
| All Critical + High priority gaps resolved | 🔶 Partial — GAP-4, GAP-56, GAP-57, GAP-58 open (Medium-High in context of GS13) |
| All Medium gaps resolved or deferred | 🔶 Partial — GAP-48, GAP-49, GAP-51, GAP-55–58 open; GAP-50 partial |
| All Low gaps addressed | 🔶 Partial — GAP-55 open; GAP-59, GAP-60 v2-deferred |
| Council review — no new unresolved tensions | 🔶 Partial — GS13 not run; T-W-BG-1, T-S-RP-1 accepted; T-BT, T16 v2 |
| gap-backlog-v5.md produced | ✅ This document |

---

## Full Status Table — All 60 Gaps

| GAP | Domain | Priority | Status |
|-----|--------|----------|--------|
| GAP-1 | MEMIT | 🔴 Critical | ⏳ Deferred (impl.) |
| GAP-2 | MEMIT | 🔴 Critical | ⏳ Deferred (impl.) |
| GAP-3 | MEMIT + Graph | 🔴 Critical | 🔶 Partial |
| GAP-4 | Orchestration | 🟠 High | 🔜 GS13 |
| GAP-5–7 | Various | 🟠 High | ✅ All resolved |
| GAP-8, 10 | Validation | 🟠 High / Medium | ✅ All resolved |
| GAP-9 | Validation + MEMIT | 🟡 Medium | 🔶 Partial → GS13 confirm |
| GAP-11, 12, 14 | SCT + MEMIT | 🟡 Medium | ✅ All resolved |
| GAP-13 | Warden + Orch. | 🟡 Medium | 🔜 GS13 v2 outline |
| GAP-15 | Validation + MEMIT | 🟡 Medium | ⏳ Deferred → GS13 confirm |
| GAP-16 | Warden + Orch. | 🟢 Low | 🔒 Accepted |
| GAP-17, 18, 19 | Various | 🟢 Low | 🔜 GS13 v2 outlines |
| GAP-20–26 | Various | 🟠 High | ✅ All resolved |
| GAP-27 | Warden + SCT | 🟠 High | ✅ Resolved (Tier conflict → GS13) |
| GAP-28 | Orch. | 🟡 Medium | ✅ Resolved |
| GAP-29 | MEMIT + Warden | 🟠 High | ✅ Resolved (GS10) |
| GAP-30, 31, 34, 35 | SCT + Warden | High/Low | ✅ All resolved (GS11) |
| GAP-32 | SCT + Warden | 🟢 Low | ⏳ v2-deferred → GS13 outline |
| GAP-33 | Warden + Graph | 🟡 Medium | ✅ Resolved (v2 GS8 + GS10 verify) |
| GAP-36, 37 | Warden + SCT | Low/Medium | ✅ All resolved (GS10) |
| GAP-38, 39 | Warden + Validation | Low/Medium | ✅ All resolved (GS12) |
| GAP-40, 41, 42 | Warden + Orch. | High/Medium | ✅ All resolved (GS10) |
| GAP-43 | SCT + Warden | 🟢 Low | ✅ Resolved (GS11) |
| GAP-44 | Warden + SCT | 🟡 Medium | ✅ Resolved (GS10) |
| GAP-45 | SCT | 🟢 Low | ⏳ v2 planning |
| GAP-46 | Warden + SCT | 🟡 Medium | ✅ Resolved (GS11) |
| GAP-47 | SCT + Warden | 🟢 Low | ✅ Resolved (GS10) |
| GAP-48 | MEMIT | 🟡 Medium | 🔜 GS13 |
| GAP-49 | Validation + MEMIT | 🟡 Medium | 🔜 GS13 |
| GAP-50 | Validation | 🟡 Medium | 🔶 Partial (T-TGA-load triage) → GS13 |
| GAP-51 | SCT + MEMIT | 🟡 Medium | 🔜 GS13 |
| GAP-52, 53, 54 | Warden / SCT | Medium/Low | ✅ All resolved (GS11) |
| GAP-55 | Warden + SCT | 🟢 Low | 🔜 GS13 (quick decision) |
| GAP-56 | Warden + SCT | 🟡 Medium | 🔜 GS13 (affects GAP-4) |
| GAP-57 | Warden + Orch. | 🟡 Medium | 🔜 GS13 (affects GAP-4) |
| GAP-58 | SCT + Warden | 🟡 Medium | 🔜 GS13 (affects GAP-4) |
| GAP-59 | SCT | 🟢 Low | ⏳ v2-deferred |
| GAP-60 | Warden | 🟢 Low | ⏳ v2-deferred |

---

*Gap Backlog v5.0 — 60 gaps tracked*
*Supersedes gap-backlog-v4.md*
*Sources: GS10, GS11, GS12 session summaries + gap-backlog-v4.md*
