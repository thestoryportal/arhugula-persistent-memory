# LLM as Database: Agent Harness Architecture
## Tension Map v5.0

> **Supersedes:** `tension-map-v4.md`
> **Delta basis:** tension-map-v4.md + GS10, GS11, GS12 session summaries
> **Closed in GS10–12:** T-SC-W-2, T-S4-N1, T-S7-N1, T-PM-vs-PA, T-TGA-load
> **New in GS10:** T-W-BG-1 (accepted), T-S-RP-1 (accepted for v1)
> **Remaining open (action required):** T15, T16, T-S4-N2 (via GAP-40 closed, residual)

---

## Status Updates from GS10–12

### Closed in GS10

**T-SC-W-2 — Write Suspension Scope vs. Governance-Ceremony Write Path**
✅ **Closed by GAP-37 resolution (GS10).** §11.8.1 now contains explicit text: governance-category W1 Ledger entries written as part of the signed reset ceremony proceed regardless of CIRCUIT_TRIPPED state; token-mediated writes do not. IC-GCO-1.

### Closed in GS11

**T-S4-N1 — Warden ↔ SCT: Rotation Registry Ordering**
✅ **Closed by GAP-46 resolution (GS11).** Stable external `operator_id` bound at first-boot CAK registration, carried unchanged across rotation. The "outgoing key governs ceremonies initiated before rotation" invariant is satisfied without requiring a new Ledger barrier contract because `operator_id` is not key-fingerprint-derived — rotation does not change the identity used for rate-limit windowing. IC-CAK-IDENTITY.

**T-S7-N1 — Warden ↔ SCT: Rate-Limit State Derived vs. Primary**
✅ **Closed by GAP-46 resolution (GS11).** Boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation added: at boot, TC verifies that `scope_update_min_interval_seconds` (per-initiator and per-agent) is strictly less than the minimum retention window for `SCOPE_UPDATED` Ledger entries. If the condition fails, boot is suspended with `RATE_LIMIT_RETENTION_CONFLICT` (SECURITY, sync, W1). IC-BOOT-RLRF.

**T-PM-vs-PA — Provenance Monitor vs. Pruning Agent Advisory Queue Priority**
✅ **Closed by GS11 spec block.** Merge policy selected: external-provenance advisories merge into the existing review queue item for the same `edge_id` rather than creating a separate item. CORE-importance facts with STALE or UNAVAILABLE provenance get priority elevation in the merged item. Both advisory reasons must be acknowledged for resolution. IC-REVIEW-QUEUE amended.

### Closed in GS12

**T-TGA-load — TGA Authority Concentration**
✅ **Closed as 📋 Accepted for v1.** Concentration of verification-artifact authorship (executable tests + three probe sub-types + sole task-specification reader) is governed by D32–D33 as an acknowledged design principle. A split would either duplicate task-spec reading authority or move the concentration to a shared intermediate representation. v2-reconsider flag set; reopens only if v1.1 operation surfaces concrete failure-mode evidence.

---

## New Tensions from GS10

### T-W-BG-1 — Break-Glass Friction vs. Incident-Response Urgency
**Specialists:** Warden (internal) | **Status:** 📋 Accepted design tradeoff

Physical-access requirement (C-BG-4) and M≥3 quorum (C-BG-2) for break-glass CAK rotation make the channel slow to activate by design. This creates a real tension with incident response requiring rapid CAK replacement when the primary CAK is compromised. **Accepted:** the break-glass channel is an extreme-case mechanism, not an operational one; its deliberate friction is the security property. Operators must ensure backup custodians are pre-arranged before this tension becomes a real incident. Documented for operator awareness; not a spec blocker.

### T-S-RP-1 — Operator-Owned Dry-Run Store vs. Warden-Audited Immutability
**Specialists:** Warden ↔ State Consistency Theorist | **Status:** 📋 Accepted for v1; v2-flagged

The `.dry-run-store/` is operator-owned (GAP-33). Warden's audit surface is metadata-only (C-DRS-6): hash anchors in the Ledger verify what was present, but cannot detect content swapped before the executor signs. Mitigated by IC-DRS-1's manifest-hash anchor in the Ledger. **Accepted for v1:** the attack model requires compromising both the executor signing process and the Ledger, which exceeds the v1 trust boundary. Flagged for v2 if content-addressed immutable storage (e.g., CAS backend) is adopted.

---

## Full Tension Map — All Tensions (v5 State)

| ID | Name | Specialists | Status |
|----|------|-------------|--------|
| T1–T12 | Session 7 integration tensions | Various | ✅ All resolved (v1.1 spec) |
| T13 | Advisory Boundedness vs. Operational Flexibility | MEMIT + Orchestration | ✅ Resolved (GS7 v3) |
| T14 | Single-Key vs. Dual-Key for Ceremony Authorization | Warden + Orchestration | ✅ Resolved (GS4 v2/v3) |
| T15 | CAK Availability vs. Ceremony Urgency | Warden + Orchestration | 🔶 Partial — GS13 v2 path + A11 |
| T16 | Ceremony-Scope Narrowness vs. Operational Batching | Warden + SCT | 🔴 v2 — GS13 outline |
| T-SC-W-1 | Audit Category vs. Lifecycle for Hold Release | SCT + Warden | ✅ Resolved (GS5 v3) |
| T-SC-W-2 | Write Suspension vs. Governance-Ceremony Write | SCT + Warden | ✅ Resolved (GS10) |
| T-S3-N1 | Ledger Ordering Underpins D87 | Warden + SCT | ✅ Resolved (GS5 v3) |
| T-S3-N2 | Push-Based Invalidation Channel | Warden + Orchestration | ✅ Resolved (GS9 v3) |
| T-S4-1 | Audit Completeness Under Roster Indirection | Warden + Validation | 📋 Absorbed |
| T-S4-2 | Roster State at Snapshot Boundaries | SCT + Validation | ✅ Resolved |
| T-S4-3 | Two-Signature Ceremony Latency for Promotion | Orchestration + Validation | 📋 v2 concern |
| T-Candidate-GS7 | Dry-Run Freshness vs. Authorship Lifecycle | MEMIT + Graph | ✅ Resolved (D-GS8-D) |
| T13-v1-GS1 | Manifest Signing Ownership (local) | MEMIT + Warden | ✅ Resolved (GS7 v3) |
| T14-v1-GS1 | Deprecation Timing vs. Compaction Cadence (local) | MEMIT + SCT | ✅ Resolved (GS7 v3) |
| T-S4-N1 | Rotation Registry Ordering | Warden + SCT | ✅ Resolved (GS11) |
| T-S4-N2 | Bootstrap-Tool Trust Asymmetry | Warden + Orchestration | 📋 Ack. — GAP-40 resolved |
| T-S7-N1 | Rate-Limit State Derived vs. Primary | Warden + SCT | ✅ Resolved (GS11) |
| T-PM-vs-PA | Provenance Monitor vs. Pruning Agent Advisory | SCT + Warden | ✅ Resolved (GS11) |
| T-TGA-load | TGA Authority Concentration | Validation | ✅ Accepted for v1 (GS12) |
| T-BT | Bounded Tunability Latent Tension | Various | 📋 v2 planning |
| T-NOTIFY-LOSS | Notification Loss Failure Mode | SCT + Orchestration | 📋 Accepted tradeoff |
| T-v2GS6-CEREMONY-DECOMP | Ceremony Atomicity vs. Decomposition | SCT + Warden | 📋 Framework axis |
| T-W-BG-1 | Break-Glass Friction vs. Incident Urgency | Warden | 📋 Accepted (GS10) |
| T-S-RP-1 | Dry-Run Store Ownership vs. Warden Immutability | Warden + SCT | 📋 Accepted for v1 (GS10) |

---

## Tensions Requiring GS13 Action

1. **T15 (CAK Availability)** — v2 resolution path (OQ-S-CAK-1 via GAP-42 break-glass partially addresses; OQ-S-CAK-2 m-of-n remains v2). GS13: A11 deployment guidance + confirm GAP-42 satisfies v1 mitigation requirement.
2. **T16 (Ceremony-Scope Narrowness)** — v2 outline only; per-Hold path is v1-specced and workable.

All other tensions are either resolved, accepted, or v2-deferred. No new High-priority tensions remain unaddressed.

---

*Tension Map v5.0 — 25 tension IDs tracked*
*Supersedes tension-map-v4.md*
*Sources: GS10, GS11, GS12 session summaries + tension-map-v4.md*
