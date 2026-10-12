# Gap Session 1 Summary — MEMIT Specialist + Graph Data Architect
## LLM as Database: Agent Harness Architecture

> **Session:** Gap Session 1 of 8
> **Domain:** MEMIT Specialist + Graph Data Architect
> **Topic:** GAP-3 v1.1 Closure Audit + v2 Outline Spec Production
> **Baseline:** v1.1 Integrated Specification
> **Date:** Gap Session 1

---

## Session Scope

This session targeted GAP-3 (Critical): the `.larql` schema versioning strategy and its
v1.1 partial closure. The session had three objectives:

1. Verify the v1.1 closure of GAP-3 is complete and internally consistent
2. Produce v2 outline spec blocks for the three remaining residual items
3. Confirm whether the `LARQL_VERSION_LEGACY` advisory path is sufficient for the
   v1→v1.1 transition

---

## Gaps Resolved

**GAP-3 (partial closure confirmed)**
The Gate enforcement layer of GAP-3 is **confirmed closed** in v1.1. Pre-check #8, the
versioned patch parser (D82), and the `larql_migration_manifest` structure in Tier 1 config
form a structurally sound enforcement chain. No seams in the enforcement mechanism itself.

---

## Gaps Partially Resolved

**GAP-3 (v2 residual)** — Three residual items now have v2 outline spec blocks:

- **(a) Migration manifest authorship ceremony** — Two-stage model (machine-draft +
  human ratification); mandatory atomicity with version counter advance.
- **(b) Deprecation ceremony and notice period policy** — 90-day standard / 14-day
  emergency floor; three pre-conditions (drain check, archive audit, notice period).
- **(c) Multi-version team deployment advisory window policy** — `LARQL_VERSION_LEGACY`
  declared a bounded transition state; three-tier accumulation escalation model
  (10 / 50 / 100 patches → warning / soft-block / hard-block).

---

## Gaps Deferred

None. All v2 items are now outlined. Threshold values (notice period days, accumulation
tier ceilings, `COMPACTION_TRANSLATION_HEAVY` percentage) remain provisional, flagged as
requiring MEMIT empirical input (dependency on GAP-1).

---

## New Gaps Surfaced

### GAP-21 — `larql_migration_manifest` Format Unspecified

| Field | Value |
|---|---|
| **Domain(s)** | MEMIT Specialist, Graph Data Architect |
| **Priority** | 🟠 High |

**Description:** The v1.1 spec names `larql_migration_manifest` as a Tier 1 config artifact
(§8.10, §13.2) and the versioned patch parser is specified to consume it (D82). But the
format of a manifest entry — what fields it contains, what the structure of a translation
rule looks like, how bucket decisions are expressed — is completely unspecified. The
parser-manifest interface contract is missing. This is not a deferred v2 item; it is an
unspecified dependency of a v1.1 component.

**Blocks:** Manifest authorship ceremony spec, compaction recovery path spec, bucket boundary
resolution for T1 translation.

**Resolution path:** The v2 outline spec block 2a (see full session transcript) proposes a
mandatory entry schema. May be resolvable as a v1.2 patch rather than waiting for full v2
work.

---

## New Tensions Surfaced

### T-NEW-1 — Advisory Boundedness vs. Operational Flexibility

**Domain boundary:** Write Engine (format discipline enforcement) ↔ Orchestration
Comparativist (operational continuity for active projects)

**Competing requirements:**

- **Write Engine requires:** `LARQL_VERSION_LEGACY` is a bounded state. Unbounded
  legacy-patch accumulation creates translation debt, compaction fidelity risk, and an
  indefinitely growing manifest maintenance burden.
- **Orchestration requires:** Teams in active development should not have agents hard-blocked
  mid-sprint because a notice period elapsed while the team was focused on a delivery
  milestone.

```
IC-PENDING: T-NEW-1 (Advisory Boundedness vs. Operational Flexibility)
Requires resolution with: MEMIT Specialist + Orchestration Comparativist
Write Engine layer must provide: Maximum acceptable legacy accumulation count
  before compaction fidelity is meaningfully degraded.
Orchestration layer must provide: The minimum operator-override window that
  preserves operational flexibility without requiring unlimited accumulation.
Status: Open. The v2 hard-block threshold (100 patches) in spec block 2c is
  a proposal only — requires MEMIT-side empirical input on compaction fidelity
  degradation rates.
```

---

## Decisions Made

| ID | Decision |
|---|---|
| **D-GAP1-A** | `LARQL_VERSION_LEGACY` is declared a **bounded transition state**, not a supported indefinite production configuration. |
| **D-GAP1-B** | Manifest authorship follows a **two-stage ceremony** (machine-draft + human ratification). Human ratification is required for all manifest entries. |
| **D-GAP1-C** | Manifest entry **must be ratified BEFORE** `current_larql_version` advances. Advance without a ratified manifest entry is a spec violation. |
| **D-GAP1-D** | T1 translation fidelity requires a bucket boundary decision for the v1.0→v1.1 float-to-enum mapping. Proposed thresholds (≥0.75 `CORE`, 0.50–0.74 `SUPPORTING`, <0.50 `INCIDENTAL`) **deferred for v2 ratification**. |

---

## Seams Identified in v1.1 Closure

| Seam | Nature | v1.1 Status | Resolution Required In |
|---|---|---|---|
| A — Manifest atomicity | Operational correctness gap | Not addressed | v2 spec |
| B — Manifest format unspecified | Missing interface contract | Not addressed — **NEW GAP-21** | v1.2 patch or v2 |
| C — T1 translation fidelity | Lossy bucket decision unresolved | Not addressed | v2 spec |
| D — Compaction abort recovery for translation failure | Missing recovery path | Partially addressed | v2 spec |
| E — Advisory accumulation | Missing escalation model | Not addressed | v2 spec |

---

## Interface Contracts Defined

**IC-MANIFEST-1** — Manifest entry schema (proposed fields):

```
from_version:              string    # Version being translated FROM
to_version:                string    # Version being translated TO
field_transformations:     []        # Ordered list of transform rules
  - field_name:            string    # Field in old format
    action:                enum      # RENAME | DROP | SPLIT | DEFAULT | BUCKET
    target_field:          string    # Target field (for RENAME/SPLIT)
    bucket_map:            object    # For BUCKET: {threshold_high, threshold_low, values}
    default_value:         any       # For DEFAULT: value to inject when field absent
authored_by:               string    # Human operator identifier
authored_at:               timestamp
ratification_signature:    string    # Operator cryptographic signature over entry hash
advance_ledger_entry_id:   string    # ID of VERSION_ADVANCED Ledger entry this enables
```

*Subject to v2 ratification.*

**IC-LEGACY-ACCUM-1** — Orchestrator token issuance path must check per-agent accumulation
tier before issuing any invocation token for agents generating legacy-version patches.

---

## New Ledger Entry Types Proposed

| Entry Type | Category | Mode |
|---|---|---|
| `VERSION_ADVANCED` | GOVERNANCE | Synchronous |
| `VERSION_DEPRECATED` | GOVERNANCE | Synchronous |
| `EMERGENCY_DEPRECATION_REQUEST` | GOVERNANCE | Synchronous, human-only |
| `LEGACY_ACCUMULATION_WARNING` | Advisory | Async |
| `LEGACY_ACCUMULATION_SOFT_BLOCK` | Advisory | Async |
| `LEGACY_ACCUMULATION_HARD_BLOCK` | — | Synchronous |
| `LEGACY_TOKEN_ISSUED_UNDER_ADVISORY` | — | Synchronous, per-token |
| `COMPACTION_TRANSLATION_HEAVY` | Advisory | Async |
| `LEGACY_EXTENSION_GRANTED` | GOVERNANCE | Synchronous |

---

## Clarification Note Recommended for v1.1

§10.2 pre-check #8 should receive an annotation (not a decision change) clarifying:

> *"The `LARQL_VERSION_LEGACY` advisory path is a bounded transition state. The migration
> manifest entry for the legacy version must be ratified before the advisory path can be
> relied upon for compaction correctness. Operation in advisory state for more than
> [notice_period] days constitutes an out-of-compliance configuration."*

---

## Advisory Sufficiency Finding

**Question:** Is `LARQL_VERSION_LEGACY` advisory sufficient for the v1→v1.1 transition?

**Answer:** The advisory path is structurally sufficient for a bounded transition window,
but two conditions must be met for safe use:

1. The `larql_migration_manifest` entry for the relevant version pair must be authored and
   ratified — including the bucket boundary decision for the T1 float-to-enum translation —
   before the advisory path is relied upon for compaction.
2. The advisory must be treated as a bounded transition state (not indefinite production),
   which the v1.1 spec does not currently enforce. That enforcement requires the accumulation
   thresholds and deprecation ceremony defined in the v2 outline spec blocks.

---

## Open Questions Carrying Into Next Session

| ID | Question | Blocked By |
|---|---|---|
| OQ-GAP1-1 | Should manifest authorship allow Architect Agent involvement (with human ratification), or is it fully outside the agent authorization model? | v2 session |
| OQ-GAP1-2 | Should a test compaction ("manifest dry-run") on a sample of legacy patches be mandatory before manifest ratification? | v2 session |
| OQ-GAP1-3 | Should the hard block (Tier 3 accumulation) allow operator extension with a signed exception record? (`LEGACY_EXTENSION_GRANTED` pattern proposed but not decided.) | T-NEW-1 resolution |
| OQ-GAP1-4 | At what accumulation count does compaction fidelity meaningfully degrade? | GAP-1 (empirical — blocked by model selection) |

---

## v2 Outline Spec Blocks Produced

Three v2 outline spec blocks were produced in full (see session transcript for complete text):

- **2a** — `larql_migration_manifest` Authorship Ceremony Spec Block
- **2b** — `larql_syntax_version` Deprecation Ceremony and Notice Period Policy Spec Block
- **2c** — `LARQL_VERSION_LEGACY` Advisory Window — Multi-Version Deployment Policy Spec Block

---

*Gap Session 1 Summary — LLM as Database: Agent Harness Architecture*
*MEMIT Specialist + Graph Data Architect — v2 Planning Input*
