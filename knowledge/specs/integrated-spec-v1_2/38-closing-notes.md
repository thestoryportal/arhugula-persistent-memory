## Closing Notes

This v1.2 specification closes the v1.1 → v1.2 iteration. v1.1 is preserved in full: every v1.1 decision, constraint, and interface contract carries forward unless explicitly marked DEPRECATED or AMENDED in this document. The v1.2 delta resolves 52 of 60 tracked gaps across the thirteen Phase 2 gap sessions (see `gap-backlog-v5.md`), closes 23 of 25 cross-domain tensions (see Appendix F), and applies fourteen ratified amendments (A1-REVISED, A2–A14; see Appendix G).

**What this spec does:**
- Defines every component and every interface between components at the single-machine reference-implementation level.
- Establishes the unified CeremonyToken authorization model (IC-SCOPE-AUTH-1) as the sole authority chain for every GOVERNANCE-class ceremony.
- Binds the Ledger, the `.vindex` overlay, and the Git repository via the State Ledger and the two-phase commit protocol, extended by the v1.2 bounded-compensation machinery (A1-REVISED).
- Specifies every operator-observable state change via the Ledger entry catalog (Appendix C), including the 50+ v1.2 additions for ceremonies, burst states, bootstrap verification, provenance, and retention.
- Documents every ratified amendment with a section pointer (Appendix G) and registers every D-number collision across parallel session tracks (Appendix H).
- Enumerates two remaining tensions (T15 partial, T16 v2-deferred) and the full open-question register (§18) with explicit dispositions for each.

**What this spec does NOT do:**
- Prescribe implementation language, framework, or runtime details.
- Select an orchestration path (A/B/C) — operator-decided per §19 and Appendix A.
- Specify values for thresholds marked provisional in §18 / GAP-1.
- Address multi-machine or distributed-trust scenarios — v2 scope (§19; T15/T16; GAP-18).
- Define the content-addressed immutable dry-run store (T-S-RP-1; v2 scope).
- Define the m-of-n CAK operational availability path (T15 full resolution; OQ-S-CAK-2; v2).

**Open gaps carrying into v2:**
- GAP-1 (empirical thresholds), GAP-2 (MEMIT architecture compatibility), GAP-3 (v2 migration path), GAP-4 (orchestration path selection), GAP-18 (multi-machine Ledger replication), remaining medium/low-priority GAP-XX items — see `gap-backlog-v5.md` for the full register.

**Carry-forward conditions:**
- v1.2 is structurally self-contained. Reading v1.1 is not required; every v1.1 decision referenced in v1.2 text appears inline or is explicitly pointed to.
- The `llm-as-database-agent-harness-framework.md` background remains the reference for the paradigm (larql, V-Index, MEMIT literature basis) and is not superseded by this spec.
- Deprecated v1.1 Ledger entry types (`HOLD_RELEASE_SIGNATURE_INVALID`, `HOLD_RELEASE_REPLAY_REJECTED`) remain chain-valid in historical Ledgers per C-DEPREC-1. Migration tooling per A7 is required for any operator who needs aggregate reporting that spans the deprecation cutoff.

**Status:** Ready for operator ratification and implementation planning. No targeted follow-on session is required for v1.2 sealing based on the assembly findings (see Appendix I). v2 extends this baseline additively.

*— End of v1.2 Integrated Specification —*
