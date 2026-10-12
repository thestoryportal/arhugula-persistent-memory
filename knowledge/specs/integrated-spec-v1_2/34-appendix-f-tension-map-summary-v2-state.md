## Appendix F — Tension Map Summary (v2 State)

Summary of the cross-domain tension register as of v1.2 sealing. Pulled verbatim from `tension-map-v5.md`. All 25 tension IDs are listed with their current disposition. 23 of 25 are ✅ Resolved or 📋 Accepted; 2 remain (T15 partial; T16 v2-deferred) and are the sole reason the spec carries an "all tensions accounted for" rather than "all tensions closed" status line.

### Resolution notation

- ✅ **Resolved** — addressed by a ratified decision, interface contract, or spec block. No further action pending.
- 📋 **Accepted** — acknowledged as a design tradeoff or operator-owned concern; no spec-level remediation. Documented for operator awareness.
- 🔶 **Partial** — v1 mitigation in place; full resolution deferred to v2.
- 🔴 **v2** — v1 outlines only; resolution is v2 scope.

### Full map

| ID | Name | Specialists | Status | Where resolved |
|----|------|-------------|--------|----------------|
| T1–T12 | Session 7 integration tensions | Various | ✅ Resolved | v1.1 spec, preserved in v1.2 |
| T13 | Advisory Boundedness vs. Operational Flexibility | MEMIT + Orchestration | ✅ Resolved | GS7 v3 |
| T14 | Single-Key vs. Dual-Key for Ceremony Authorization | Warden + Orchestration | ✅ Resolved | GS4 v2/v3 (D-GAP4-A, IC-SCOPE-AUTH-1) |
| T15 | CAK Availability vs. Ceremony Urgency | Warden + Orchestration | 🔶 Partial | GS13 v2 path; A11 v1 deployment guidance; GAP-42 break-glass partial mitigation |
| T16 | Ceremony-Scope Narrowness vs. Operational Batching | Warden + SCT | 🔴 v2 | GS13 outline; per-Hold path v1-specced |
| T-SC-W-1 | Audit Category vs. Lifecycle for Hold Release | SCT + Warden | ✅ Resolved | GS5 v3 |
| T-SC-W-2 | Write Suspension vs. Governance-Ceremony Write | SCT + Warden | ✅ Resolved | GS10 (§11.8.1, IC-GCO-1) |
| T-S3-N1 | Ledger Ordering Underpins D87 | Warden + SCT | ✅ Resolved | GS5 v3 |
| T-S3-N2 | Push-Based Invalidation Channel | Warden + Orchestration | ✅ Resolved | GS9 v3 (D111) |
| T-S4-1 | Audit Completeness Under Roster Indirection | Warden + Validation | 📋 Absorbed | — |
| T-S4-2 | Roster State at Snapshot Boundaries | SCT + Validation | ✅ Resolved | — |
| T-S4-3 | Two-Signature Ceremony Latency for Promotion | Orchestration + Validation | 📋 v2 concern | — |
| T-Candidate-GS7 | Dry-Run Freshness vs. Authorship Lifecycle | MEMIT + Graph | ✅ Resolved | D-GS8-D |
| T13-v1-GS1 | Manifest Signing Ownership (local) | MEMIT + Warden | ✅ Resolved | GS7 v3 |
| T14-v1-GS1 | Deprecation Timing vs. Compaction Cadence (local) | MEMIT + SCT | ✅ Resolved | GS7 v3 |
| T-S4-N1 | Rotation Registry Ordering | Warden + SCT | ✅ Resolved | GS11 (IC-CAK-IDENTITY) |
| T-S4-N2 | Bootstrap-Tool Trust Asymmetry | Warden + Orchestration | 📋 Acknowledged | GAP-40 resolved; residual accepted |
| T-S7-N1 | Rate-Limit State Derived vs. Primary | Warden + SCT | ✅ Resolved | GS11 (IC-BOOT-RLRF, §13.5 step 5a) |
| T-PM-vs-PA | Provenance Monitor vs. Pruning Agent Advisory | SCT + Warden | ✅ Resolved | GS11 (IC-REVIEW-QUEUE amended, §15.1) |
| T-TGA-load | TGA Authority Concentration | Validation | ✅ Accepted for v1 | GS12 (D32/D33 acknowledged; v2-reconsider flagged) |
| T-BT | Bounded Tunability Latent Tension | Various | 📋 v2 planning | — |
| T-NOTIFY-LOSS | Notification Loss Failure Mode | SCT + Orchestration | 📋 Accepted tradeoff | D111 one-attempt-before-TTL boundary |
| T-v2GS6-CEREMONY-DECOMP | Ceremony Atomicity vs. Decomposition | SCT + Warden | 📋 Framework axis | — |
| T-W-BG-1 | Break-Glass Friction vs. Incident Urgency | Warden | 📋 Accepted | GS10 — deliberate security property; A11 precondition |
| T-S-RP-1 | Dry-Run Store Ownership vs. Warden Immutability | Warden + SCT | 📋 Accepted for v1 | GS10 — IC-DRS-1 metadata-only audit; v2-flagged |

### Tensions requiring action beyond v1.2

Two remain:

**T15 (CAK Availability vs. Ceremony Urgency).** Partial in v1.2: A11 deployment-precondition text requires operators to pre-arrange break-glass custodians before declaring harness operational. GAP-42 (break-glass channel) provides a v1 mitigation path for the full CAK-loss scenario. Full resolution (m-of-n CAK with operational-latency budget) is v2 scope per OQ-S-CAK-2.

**T16 (Ceremony-Scope Narrowness vs. Operational Batching).** v2-scope. v1.2 ships with per-Hold ceremony scope. Batch-release path (GS13 outline) is documented but not specced. No v1.2 operator action required; operators accepting per-Hold-ceremony operational cost are fully supported.

All other tensions are either resolved (✅), accepted by explicit design decision (📋), or absorbed into later architecture (✅ / 📋 absorbed). No High-priority tension remains unaddressed in the v1.2 cross-domain register.

---

