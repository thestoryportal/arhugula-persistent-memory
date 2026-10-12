# LLM as Database: Agent Harness Architecture
## Gap Session Schedule v4.0

> **Supersedes:** `gap-session-schedule-v3.md`
> **Source backlog:** `gap-backlog-v4.md` (39 gaps, post all non-council sessions)
> **Status:** Draft
> **Total arc:** 13 sessions (GS1–GS13) — 9 completed, 4 remaining

---

## Completed Sessions (Reference)

| Session | Gaps | Status |
|---------|------|--------|
| GS1 | GAP-3 (partial) | ✅ v1 schedule |
| GS2 | GAP-6, GAP-7 | ✅ v1 schedule |
| GS3 | GAP-5 | ✅ v1 schedule |
| GS4 | GAP-8 residual / GAP-10 (v1); T14 / GAP-26 (v2/v3) | ✅ Both schedules |
| GS5 | GAP-21, GAP-24, GAP-25 + SCT review + A-batch | ✅ v3 schedule |
| GS6 | GAP-22, GAP-23 | ✅ v3 schedule |
| GS7 | T13, GAP-27, GAP-20 + A4–A9 | ✅ v3 schedule |
| GS8 | GAP-8 (final), GAP-10 (final) | ✅ v3 schedule |
| GS9 | GAP-11, GAP-12, GAP-14, GAP-28 | ✅ v3 schedule |

**Not yet run:**
- GS10 (v3 schedule full council) — absorbed into GS13 below with updated scope

---

## What Changed: v3 → v4

Nine sessions produced 11 new gaps (GAP-29 through GAP-39) and surfaced T16 and
two additional open tensions. These require four new sessions before Phase 2 can close.
The previously unrun GS10 (v3 full council) is carried forward as GS13 with its scope
updated to reflect current gap states.

**Previous skipped full council sessions (v1 GS7, v1 GS8):** Work in scope for those
sessions has been superseded — GAP-1/2 formally deferred; GAP-4/13/17/18/19 are GS13
targets; GAP-16 accepted as deployment-specific. No separate re-run required.

---

## Dependency Classification (v4)

**No upstream gap dependency (parallelizable):**
GS10, GS11, GS12 are independent of each other and of GS13.

**Run before GS13:** GS10–GS12 preferred first so GS13's full council has accurate
current state. GS13 is not hard-blocked on them, but the v2 outline blocks benefit
from knowing what new gaps were resolved.

---

## Council Flag

| Session | Council Required? | Rationale |
|---------|-------------------|-----------|
| GS10 | YES | GAP-29 spans Warden + MEMIT + Graph; GAP-37 is Warden + SCT; GAP-33 is Warden + Graph. Three-domain minimum. |
| GS11 | YES | GAP-31 and GAP-34 require Warden co-owner alongside SCT primary. |
| GS12 | No | GAP-39 is single-specialist Validation. GAP-38 could be folded but is short enough for GS12 if Warden + Orchestration attend. See note. |
| GS13 | YES — Full council | All six specialist voices needed: path specs (Orchestration + Warden + SCT + MEMIT), v2 outlines (Warden + Orchestration + SCT), T15 resolution. |

**Note on GS12:** GAP-38 (cross-invocation aggregate detection, Warden + Orchestration) and
GAP-39 (clock injection, Validation) are bundled for efficiency. Invoke `framework-council`
with Warden, Orchestration, and Validation; all three are short resolutions.

---

## Session Schedule

---

### ✅ GS1–GS9 — COMPLETED
*(See summary files in KB)*

---

### GS10 — NEXT
**Gaps:** GAP-29, GAP-33 (resolved — verify), GAP-36, GAP-37, GAP-40, GAP-41, GAP-42, GAP-44, GAP-47
**Primary skill:** `framework-council` (Warden primary; MEMIT Specialist + Graph Data Architect + State Consistency Theorist secondary)
**Council:** YES
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** All nine are Warden-primary or Warden co-owned with no upstream gap dependency. GAP-40/41/42 are v2 GS4 new gaps directly in the Warden + Orchestration domain. GAP-44 (GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE classification) needs Warden review. GAP-47 (dry-run pruning ceremony) is a quick Appendix C integration. GAP-29 (W3 consolidation + manifest lattice) is the highest-priority item — W3 policy from GAP-29b directly informs whether GAP-44 gets W3 eligibility.

---

### GS11
**Gaps:** GAP-30, GAP-31, GAP-34, GAP-35, GAP-43, GAP-46, GAP-52, GAP-53, GAP-54
**Primary skill:** `framework-council` (State Consistency Theorist primary; Warden co-owner on GAP-31, GAP-34, GAP-46, GAP-52, GAP-54)
**Council:** YES
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why expanded:** Six new gaps from v2 sessions (GAP-43, GAP-46, GAP-52, GAP-53, GAP-54) join the original four. All are SCT-primary or SCT co-owned. GAP-46 (ceremony_initiator_id under rotation) relates directly to GAP-27's rate-limit model and T-S4-N1 (rotation registry ordering) — resolving GAP-46 and closing T-S4-N1 belong in the same session. GAP-52 (archive key-lifecycle) needs Warden alongside SCT. T-S7-N1 (rate-limit retention conflict) can also be resolved here alongside GAP-46.

---

### GS12
**Gaps:** GAP-38, GAP-39
**Primary skill:** `framework-council` (Warden + Orchestration Comparativist for GAP-38; Validation Contract Architect for GAP-39)
**Council:** YES (three specialists)
**Est. length:** Short
**Model:** Sonnet 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** Both are short, bounded, no upstream dependencies. GAP-38 (aggregate SCOPE_HASH_MISMATCH detection) is Warden + Orchestration and closes the remaining gap in the scope-update threat model. GAP-39 (constitutional test clock dependency) is Validation standalone. Three specialists in one short session.

---

### GS13 — Full Council
**Gaps:** GAP-4, GAP-9 (deferral), GAP-13, GAP-15 (deferral), GAP-17, GAP-18, GAP-19, T15, OQ-SC3
**Primary skill:** `framework-council` (all six specialists)
**Council:** YES — full multi-domain
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why last:** Contingent path specs (GAP-4) and v2 outlines reference decisions from GS10–GS12. GAP-19 v2 outline must account for the mint-once Tier 1 `ceremony_authorization_key_anchor` interactions defined in GS5. OQ-SC3 (stale Layer 4 fact reconciliation workflow) is a GS9 carry-forward that fits naturally alongside GAP-13 (Genesis automation policy). T-S4-3 (promotion ceremony coordination) should be triaged for v2 or GS13 acceptance.

---

## Summary Table — GS10 Through GS13

| Session | Gaps | Primary Skill | Council | Est. Length |
|---------|------|---------------|---------|-------------|
| GS10 | GAP-29, 36, 37, 40, 41, 42, 44, 47 (+ GAP-33 verify) | `framework-council` (Warden + MEMIT + Graph + SCT) | YES | Long |
| GS11 | GAP-30, 31, 34, 35, 43, 46, 52, 53, 54 | `framework-council` (SCT + Warden) | YES | Long |
| GS12 | GAP-38, 39 | `framework-council` (Warden + Orchestration + Validation) | YES | Short |
| GS13 | GAP-4, 9, 13, 15, 17–19, 27(Tier), 32, 48–51, T15, OQ-SC3 | `framework-council` (all six) | YES | Long |

**Remaining sessions:** 4 | **All council sessions:** 4

---

## Gap Disposition — All New Gaps (GAP-29 through GAP-54)

| GAP | Priority | Status | Assigned |
|-----|----------|--------|----------|
| GAP-29 | 🟠 High | 🔴 Open | GS10 |
| GAP-30 | 🟡 Medium | 🔴 Open | GS11 |
| GAP-31 | 🟡 Medium | 🔴 Open | GS11 |
| GAP-32 | 🟢 Low | ⏳ v2-deferred | GS13 outline |
| GAP-33 | 🟡 Medium | ✅ Resolved (v2 GS8) | GS10 verify only |
| GAP-34 | 🟡 Medium | 🔴 Open | GS11 |
| GAP-35 | 🟢 Low | 🔴 Open | GS11 |
| GAP-36 | 🟢 Low | 🔴 Open | GS10 |
| GAP-37 | 🟡 Medium | 🔴 Open | GS10 |
| GAP-38 | 🟢 Low | 🔴 Open | GS12 |
| GAP-39 | 🟡 Medium | 🔶 Partial | GS12 |
| GAP-40 | 🟠 High | 🔴 Open | GS10 |
| GAP-41 | 🟡 Medium | 🔴 Open | GS10 |
| GAP-42 | 🟡 Medium | 🔴 Open | GS10 |
| GAP-43 | 🟢 Low | 🔴 Open | GS11 |
| GAP-44 | 🟡 Medium | 🔴 Open | GS10/GS11 |
| GAP-45 | 🟢 Low | ⏳ v2 planning | — |
| GAP-46 | 🟡 Medium | 🔴 Open | GS11 |
| GAP-47 | 🟢 Low | 🔴 Open | GS10 |
| GAP-48 | 🟡 Medium | 🔴 Open | GS13 |
| GAP-49 | 🟡 Medium | 🔴 Open | GS13 |
| GAP-50 | 🟡 Medium | 🔴 Open | GS13 |
| GAP-51 | 🟡 Medium | 🔴 Open | GS13 |
| GAP-52 | 🟡 Medium | 🔴 Open | GS11 |
| GAP-53 | 🟢 Low | 🔴 Open | GS11 |
| GAP-54 | 🟡 Medium | 🔴 Open | GS10/GS11 |

---

*Gap Session Schedule v4.0 (amended post-v2 reconciliation) — 13 sessions (GS1–GS13)*
*Supersedes gap-session-schedule-v3.md*
*Sources: gap-backlog-v4.md · tension-map-v4.md · all v1/v2/v3 gap session summaries*
