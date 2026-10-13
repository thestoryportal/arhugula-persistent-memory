## Appendix H — D-Number Collision Register (D89–D103)

Parallel v1 / v2 / v3 gap-session tracks assigned D-numbers independently for local decisions, producing collisions in the D89–D103 range. This appendix registers every such D-number so that downstream readers can disambiguate. v1.2 citation style for any D-number in this range uses **session reference + content description** rather than bare D-number to eliminate ambiguity.

### Convention

- **Baseline v1.1:** D1 through D80 were assigned during the seven-session Council arc (Schema through Integration) and are unique by construction.
- **v1.1 IC Review Session:** D81 through D90 were assigned during the v1.1 Interface Contract Review; these are authoritative v1.1 decisions.
- **Phase 2 gap sessions:** GS4 through GS13 on parallel v2 and v3 tracks reused the D89+ range for local decisions before the collision pattern was detected. The register below records every local assignment.

### Register

| D-Number | Source | Content Summary | Disambiguation Key |
|---|---|---|---|
| **D81** | v1.1 IC Review | Gate pre-check #8 — `larql_syntax_version` header validation. IC-GATE-8, C-GATE-1. | `v1.1-D81 — Gate version check` |
| **D82** | v1.1 IC Review | Versioning semantics — forward/backward/legacy policy. | `v1.1-D82 — versioning semantics` |
| **D83** | v1.1 IC Review | Write Engine drift_state object. IC-WE-1, C-WE-1. | `v1.1-D83 — IC-WE-1 drift state` |
| **D84** | v1.1 IC Review | Circuit breaker reset ceremony. IC-TC-RESET. | `v1.1-D84 — IC-TC-RESET baseline` |
| **D85** | v1.1 IC Review | Two-value timeout model. IC-TC-TIMEOUT, C-GATE-2. | `v1.1-D85 — IC-TC-TIMEOUT` |
| **D86** | v1.1 IC Review | Compaction probe stratified sampling. IC-OC-PROBE, C-OC3. | `v1.1-D86 — IC-OC-PROBE` |
| **D87** | v1.1 IC Review | Scope update ceremony. IC-SCOPE-UPDATE baseline. | `v1.1-D87 — IC-SCOPE-UPDATE baseline` |
| **D88** | v1.1 IC Review | Corpus author interface. IC-CORPUS-AUTH baseline. | `v1.1-D88 — IC-CORPUS-AUTH baseline` |
| **D89** *(v1.1)* | v1.1 IC Review | Retention lifecycle — IC-LDG-RETAIN baseline. Archival format "1.0". | `v1.1-D89 — IC-LDG-RETAIN baseline` |
| **D89** *(v3 GS7)* | GAP-27 ratification (GS7 v3) | `scope_update_min_interval_seconds` Tier 1 field; rate-limit-precedes-signature ordering. | `GS7-v3-D89 — SCOPE_UPDATED rate limit` |
| **D90** *(v1.1)* | v1.1 IC Review | Content classification mixed — IC-GATE-9 structured rejection with split_guidance. | `v1.1-D90 — IC-GATE-9` |
| **D90** *(GS3 reference in GS4 v2)* | GS3 / GS4 v2 | Scope update ceremony internal reference (per GS4 v2 §"Ceremony types in unified scope"). | `GS4-v2-D90-ref — scope update ceremony` |
| **D91** | GS3 (origin) / ratified GS9 v3 as D111 | Best-effort scope-update notification; at-least-one-attempt-before-TTL. Final TTL = 60s (Tier 3, 10s Tier 1 floor). Agent responsibility reaffirmed — notification is a performance hint, not a safety mechanism. | `GS9-v3-D111 — D91 ratification (scope notification TTL)` |
| **D92** | GS4 CeremonyToken model (informal attribution via GS8 v2) | Component of the CeremonyToken model (envelope structure — precise scoping per GS8 v2 reference "D92–D96 CeremonyToken model"). [COUNCIL-FLAG: D92 is not labeled as a formal decision in GS4 v2; attribution is indirect via downstream citation. Session reference + content description is the authoritative disambiguator.] | `GS4-v2-CeremonyToken-envelope (informal D92)` |
| **D93** *(v3 GS8)* | GS8 v3 | Corpus author registry adopted — Tier 2 `corpus-author-registry/`; Tier 1 narrowed to `corpus_author_bootstrap_identity`. | `GS8-v3-D93 — corpus-author-registry` |
| **D94** | GS8 v3 | Meta-* corpus extension cadence — 90-day advisory / 180-day enforced (`HEALTH_SCORE_STALE`). | `GS8-v3-D94 — corpus cadence tiers` |
| **D95** | GS8 v3 | Five Day-0 deployment preconditions for corpus initialization; `CORPUS_INIT_STATE` Ledger entry. | `GS8-v3-D95 — corpus init preconditions` |
| **D96** | GS8 v3 | Dual-signal constitutional test tagging (directory + module markers). | `GS8-v3-D96 — constitutional test tagging` |
| **D97** | GS8 v3 | Five qualification criteria Q1–Q5 for constitutional test promotion. | `GS8-v3-D97 — Q1–Q5 qualification` |
| **D98** *(v3 GS8)* | GS8 v3 | Constitutional test promotion via standard Tier 2 versioned additive pattern; single-operator signature in v1.1; qualification attestation block. | `GS8-v3-D98 — promotion ceremony` |
| **D98** *(v3 GS5)* | GS5 v3 | `SCHEMA_DEPRECATION_ENACTED` Ledger entry + C-DEPREC-1/2/3. A7 application. | `GS5-v3-D98 — schema deprecation machinery` |
| **D99** *(v2 GS9)* | GS9 v2 | Corpus author registry expiry — two-point enforcement; no mid-run revocation. GAP-8 residual close. | `GS9-v2-D99 — corpus author expiry` |
| **D99** *(v3 GS9)* | GS9 v3 | Layer 4 external document provenance tracking — mandatory `external_provenance` block. GAP-11 core decision. | `GS9-v3-D99 — external provenance tracking` |
| **D100** *(v2 GS9)* | GS9 v2 | Q5 weak-check — `CONSTITUTIONAL_FAILURE` field pair (`invariant_statement` + `failure_assertion_message`). A14. | `GS9-v2-D100 — Q5 weak-check` |
| **D100** *(v3 GS9)* | GS9 v3 | Provenance-record storage: two locations (patch metadata + Ledger entry `EXTERNAL_PROVENANCE_RECORDED`). | `GS9-v3-D100 — provenance storage` |
| **D101** *(v3 GS5)* | GS5 v3 | `DEPENDENCY_HOLD_RELEASED_SIGNED` formalized as GOVERNANCE/sync Appendix C entry with CeremonyToken integration. release_reason enum finalized as 4-value closed set. GAP-21. | `GS5-v3-D101 — HOLD_RELEASE_SIGNED formalization` |
| **D101** *(v3 GS9)* | GS9 v3 | Staleness is advisory, never blocking, at detection time. Three-state model FRESH/STALE/UNAVAILABLE. No auto-rewrite of Layer 4 facts. | `GS9-v3-D101 — staleness advisory` |
| **D102** *(v3 GS5)* | GS5 v3 | Degraded Orchestrator during reset ceremony — stratified response; narrow W3 carve-out; IC-TC-RESET-DEGRADED. GAP-24. | `GS5-v3-D102 — orchestrator degraded reset` |
| **D102** *(v3 GS9)* | GS9 v3 | Pruning Agent `external_source_audit` sub-routine. Cadence, per-fact override, `EXTERNAL_AUDIT_SUSPENDED` isolation. | `GS9-v3-D102 — pruning audit sub-routine` |
| **D103** *(v3 GS5)* | GS5 v3 | Scope Registry Reconciliation path — post-boot Orchestrator phase; signature reverification against current CAK anchor. IC-SCOPE-RECONCILE. GAP-25. | `GS5-v3-D103 — scope reconciliation` |
| **D103** *(v3 GS9)* | GS9 v3 | Two-tier Ledger retention governance — Tier 1 `ledger_retention_floor` (immutable-downward, 7y default) + Tier 3 `ledger_active_period` (90d default, 30d floor). | `GS9-v3-D103 — retention tiers` |

### Beyond the collision range

D104–D111 are unique to GS9 v3 and do not collide with parallel-track assignments. They are listed for completeness of the retention / consistency-parameters cluster:

| D-Number | Source | Content Summary |
|---|---|---|
| **D104** | GS9 v3 | Archive format `ledger-archive/v1` — zstd compression, SHA-256 per-entry, Merkle root, chain-link anchors. GAP-12. |
| **D105** | GS9 v3 | `PROJECT_CLOSED` synchronous + async archival; `FINAL_STATE_SNAPSHOT` atomic pair; `PROJECT_ARCHIVE_PENDING` / `PROJECT_ARCHIVED` / `PROJECT_ARCHIVE_SLA_BREACHED`. IC-RETENTION1. |
| **D106** | GS9 v3 | WAL flush policy — two-mode, keyed to fact importance class. GAP-14 core. |
| **D107** | GS9 v3 | Light Ledger chain verification at every 100 entries (retained from v1.1). |
| **D108** | GS9 v3 | Full Ledger chain verification at 10,000 entries OR 24 hours; audit-mode. |
| **D109** | GS9 v3 | Async threshold out-of-band sync SLA made explicit. |
| **D110** | GS9 v3 | All thresholds in this cluster are Tier 3 tunable with Tier 1 floor. |
| **D111** | GS9 v3 | D91 ratified final — scope-update notification at-least-one-attempt-before-TTL; 60s default TTL; Tier 3 tunable / 10s Tier 1 floor. |

### Citation guidance for downstream documents

When citing any D-number in the D89–D103 collision range, use one of the following forms:

1. **Session-qualified:** `GS9-v3-D99` or `GS9-v2-D99` — unambiguous.
2. **Content-qualified:** `D99 (external provenance tracking)` or `D99 (corpus author expiry)` — unambiguous.
3. **Both:** `GS9-v3-D99 (external provenance tracking)` — unambiguous and redundantly safe.

Avoid bare `D99`, `D100`, `D101`, `D102`, `D103`, `D90`, `D89` in cross-document references. Within a single session summary, bare D-numbers are fine because the session context resolves ambiguity.

---

