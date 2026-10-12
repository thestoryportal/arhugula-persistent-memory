# Framework Council — Review Checkpoint Session Summary
## Post-Gap Sessions 1–3
### LLM as Database: Agent Harness Architecture

> **Session type:** Council Review Checkpoint
> **Scope:** Gap Sessions 1, 2, 3 — verification, consistency check, tension map update
> **Status:** Draft
> **Basis:** gap-session-1-summary.md, gap-session-2-summary.md, gap-session-3-summary.md,
>   tension-map-v1.md, gap-backlog-v1.md

---

## Decisions Made

| ID | Decision |
|---|---|
| D-CRC-1 | GAP-ID naming collision resolved. Canonical numbering established in gap-backlog-v2.md. GS1's "GAP-21" = canonical GAP-20; GS2's GAP-20 through GAP-23 = canonical GAP-21 through GAP-24; GS3's GAP-24 through GAP-27 = canonical GAP-25 through GAP-28. |
| D-CRC-2 | GAP-1 and GAP-2 formally deferred to implementation phase. Rationale: resolution requires empirical testing against a selected target model; specification work alone cannot resolve them. All threshold values remain explicitly provisional (OQ-W1, OQ-W2). |
| D-CRC-3 | GS2 Amendment A1 (TC compensation exemption from write-token suspension) must be strengthened to bound compensation operations to strict reversal of the prior committed write only. As written in the GS2 summary, A1 creates an unbounded write path under READ_ONLY mode. Required amendment language recorded in this summary. |
| D-CRC-4 | GAP-26 (canonical) resolution must define a unified ceremony authorization framework covering all three ceremony types identified in GS1–3: manifest ratification, Hold release, and scope update ceremony. Resolution must not produce a ceremony-type-specific model that requires three separate re-specifications. |
| D-CRC-5 | T13 (Advisory Boundedness vs. Operational Flexibility) promoted to tension map as T13. Requires MEMIT Specialist + Orchestration Comparativist gap session before Phase 2 can close. |
| D-CRC-6 | T14 (Single-Key vs. Dual-Key for Ceremony Authorization) promoted to tension map as T14. Can be co-resolved with GAP-26 in GS4. |

---

## Constraints Established

| ID | Constraint |
|---|---|
| C-CRC-1 | GAP-26 (canonical) resolution must cover all ceremony types (manifest ratification, Hold release, scope update). A ceremony-specific authorization model that does not generalize is a spec violation of D-CRC-4. |
| C-CRC-2 | IC-TC-RESET must receive a placeholder amendment noting dependency on GAP-26 resolution for its ceremony authorization key model. Until GAP-26 is resolved, IC-TC-RESET's authorization key model is underspecced. |
| C-CRC-3 | Amendment A1 (§11.8.1) must include the clause: "A compensation write that would produce any weight change beyond the reversal of the prior committed operation MUST be rejected and treated as a TC fault, triggering an additional circuit trip event." |

---

## Gaps Verified Closed

| GAP | Session | Resolution |
|---|---|---|
| GAP-5 | GS3 | D87 / §10.9 / §14.3 / IC-SCOPE-UPDATE — verified sound |
| GAP-6 | GS2 | D84 / §11.8.1 / IC-TC-RESET — verified sound (A1 amendment required) |
| GAP-7 | GS2 | D85 / §11.5.1 / IC-TC-TIMEOUT — verified sound |

---

## Inconsistencies Found

| ID | Description | Required Action |
|---|---|---|
| INCON-1 | GS2 Amendment A1 does not bound TC compensation to reversal-only. As written, creates an unbounded write path under READ_ONLY mode. | Amend §11.8.1 A1 with reversal-only bounding language (D-CRC-3, C-CRC-3). |
| INCON-2 | GAP-ID naming collision: GS1's "GAP-21" and GS2's "GAP-21" refer to different gaps. | Resolved by D-CRC-1; canonical IDs established in gap-backlog-v2.md. |

---

## Tensions Updated

| Tension | Prior Status | New Status | Action |
|---|---|---|---|
| T5 | 🔶 Partial (OQ-S4 open) | 🔶 Structural resolution confirmed (D87, closes OQ-S4) | Residual seams: GAP-25 through GAP-28 (canonical) |
| T7 | ✅ Resolved (OQ-TPC1 noted as remaining) | ✅ Core tension resolved (D85, closes OQ-TPC1) | Residual: GAP-23 for Genesis Hold lifecycle |
| Pre-T5 | ⚠️ Partially resolved | ⚠️ Unchanged | GS1 improved versioning sub-gap; extension proposal pathway still unspecced |
| T12 | ⚠️ Unlocatable | ⚠️ Unchanged | Not addressed in GS1–3 |

---

## New Tensions Added to Tension Map

| ID | Name | Specialists | Status |
|---|---|---|---|
| T13 | Advisory Boundedness vs. Operational Flexibility | MEMIT + Orchestration | Open — gap session required |
| T14 | Single-Key vs. Dual-Key for Ceremony Authorization | Warden + Orchestration | Open — gap session required (combine with GS4) |

---

## Gaps Introduced (Canonical IDs)

| GAP | Domain | Priority | Source |
|---|---|---|---|
| GAP-20 | MEMIT + Graph | 🟠 High | GS1 |
| GAP-21 | State Consistency + Warden | 🟠 High | GS2 |
| GAP-22 | State Consistency | 🟠 High | GS2 |
| GAP-23 | State Consistency | 🟠 High | GS2 |
| GAP-24 | State Consistency + Warden | 🟡 Medium | GS2 |
| GAP-25 | State Consistency + Warden | 🟠 High | GS3 |
| GAP-26 | Warden | 🟠 High | GS3 |
| GAP-27 | Warden + State Consistency | 🟠 High | GS3 |
| GAP-28 | Orchestration | 🟡 Medium | GS3 |

---

## Open Questions Carrying Forward

| ID | Question | Blocked By |
|---|---|---|
| OQ-GAP1-1 | Can Architect Agent participate in manifest authorship (with human ratification)? | v2 session |
| OQ-GAP1-2 | Is test compaction ("dry-run") mandatory before manifest ratification? | v2 session |
| OQ-GAP1-3 | Should hard block (Tier 3 accumulation) allow operator extension with signed exception? | T13 resolution |
| OQ-GAP1-4 | At what accumulation count does compaction fidelity meaningfully degrade? | GAP-1 (empirical) |
| OQ-S-GAP26-1 | Physical storage contract for ceremony authorization key material? | GAP-26 / T14 resolution |
| OQ-S-GAP26-2 | Retention policy and rotation cadence for operator signing key material? | GAP-26 resolution |
| OQ-S-GAP26-3 | Must ceremony authorization key be separate from Orchestrator first-boot key (§10.5)? | T14 — core question |
| OQ-S-GAP27-1 | Per-`agent_id` or global rate limit for scope update ceremonies? | GAP-26 resolution |
| OQ-S-GAP28-1 | Should `SCOPE_UPDATED` carry `scope_change_type` enum to enable per-type notification? | GAP-28 resolution |

---

## Amendment Obligations (Required Before v1.2 or v2 Integration)

| Ref | Section | Amendment |
|---|---|---|
| A1-REVISED | §11.8.1 | TC compensation exemption bounded to reversal-only (D-CRC-3, C-CRC-3) |
| A2-GS2 | §11.8.1 | Precondition check error handling (from GS2 summary, no change to original) |
| A3-IC-TC-RESET | IC-TC-RESET | Placeholder noting ceremony authorization key dependency on GAP-26 (C-CRC-2) |
| A4-§14.3 | §14.3 | Replace 3 consecutive → 2 consecutive `SCOPE_HASH_MISMATCH` escalation (D88) |
| A5-§10.9 | §10.9 | Add ceremony authorization verification requirement (D90) |
| A6-§10.9 | §10.9 | Add rate limit requirement (D89) |
| A7-Appendix-C | Appendix C | Add: DEPENDENCY_HOLD_RELEASED_SIGNED, HOLD_RELEASE_REJECTED, SCOPE_UPDATE_RATE_EXCEEDED, SCOPE_MISMATCH_ESCALATED |
| A8-Appendix-C | Appendix C | Add cross-category rationale annotation for circuit breaker workflow entries (GS2 T-NEW-1) |

---

## Phase 2 Exit Criteria — Status

| Criterion | Status |
|---|---|
| All Critical and High priority gaps resolved | ❌ Not met |
| All Medium gaps resolved or explicitly deferred with rationale | ❌ Not met |
| All Low gaps addressed or accepted as implementation-time | 🔶 Partial (all four accepted or deferred) |
| Most recent council review produced no new unresolved tensions | ❌ Not met (T13, T14 introduced) |
| `gap-backlog-v2.md` updated with final status of all gaps | ✅ Produced this session |

**Phase 2 cannot close.** Minimum next actions: GS4 (T14 + GAP-26), GS5 (GAP-25, GAP-21, A1 revision), GS6 (GAP-22, GAP-23), GS7 (T13).

---

## Recommended Gap Session Sequencing

| Session | Specialists | Topics |
|---|---|---|
| GS4 | Warden + Orchestration | T14, GAP-26 — ceremony authorization unified model |
| GS5 | State Consistency + Warden | GAP-25, GAP-21, A1 revised amendment |
| GS6 | State Consistency | GAP-22, GAP-23 — Genesis timeout field, Hold lifecycle |
| GS7 | MEMIT + Orchestration | T13 — advisory boundedness vs. operational flexibility |
| GS8 | Validation | GAP-8, GAP-10 — corpus policy, constitutional test classification |

---

*Council Review Checkpoint — Post-Gap Sessions 1–3*
*Framework Council — LLM as Database: Agent Harness Architecture*
*gap-backlog-v2.md produced; canonical GAP IDs established; two tensions promoted; one inconsistency found and remediated*
