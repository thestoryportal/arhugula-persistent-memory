## 19. v2 Scope Targets

v2 is additive, not corrective. The v1.2 design does not prevent any v2 feature; it simply does not include them. All deferrals are anchored to a GAP or OQ identifier for traceability.

**Distributed trust:**
- Multi-machine harness with Ledger replication and distributed consensus (GAP-18).
- Cross-machine token federation.
- Multi-operator (quorum) Tier 2 signing.
- Remote attestation.

**Key lifecycle management:**
- OOK and CAK key rotation ceremonies with full dependency map (GAP-19). In v1.2 the §23.3 break-glass channel is the sole CAK-replacement mechanism.
- Operator signing key rotation and revocation (full PKI).
- Orchestrator key rotation.
- Cross-project key sharing policies.
- Delegation tokens for nested sub-agent invocations.
- CAK availability m-of-n path (OQ-S-CAK-2 / T15 v2).
- Retired-key revocation metadata semantics: retired-clean vs. retired-compromised classification for archive-bundle signing keys (GAP-60).

**Agent-to-agent trust:**
- Peer agent review delegation token design (GAP-20 — authorization model for D37 Step 2 escalation second Coder Agent).

**Ceremony scope extensions:**
- Batch Genesis Hold release and multi-Hold ceremony scoping (T16).
- Voluntary Write Lock release and inter-agent negotiation (GAP-17, OQ-CW1).
- Further scope-update rate-limit policy evolution (GAP-32).

**Formal enforcement upgrades:**
- Pre-receive Git hooks (prevent-at-write for Tier 3).
- Stronger sandbox attestation.
- Hardware-backed key storage (TPM, HSM).

**Verification scale:**
- Sampled-verification design for Ledger chains exceeding 10M entries (GAP-59 / GAP-53).

**Validation architecture:**
- TGA split into TGA-Test / TGA-Probe (T-TGA-load v2-reconsider; activates only on v1.2 operational evidence).
- Self-referential probing: probes whose judge model is itself subject to `.vindex` writes (GAP-49).

**Archival extensions:**
- External cold-storage export for `.larql` and Ledger archives.
- Project-to-project trust transfer for shared sealed corpora.
- Content-addressed immutable storage for `.dry-run-store/` (T-S-RP-1 v2-flag).

**Automation extensions:**
- Genesis automation — secondary LLM reviewer as human-review proxy (OQ-S5 / GAP-13).

**Schema versioning extensions:**
- OQ-W6 residual — `.larql` schema version migration path authorship, deprecation ceremony, multi-version team deployment.

**Observability conventions:**
- Aggregate-detection entry type convention (GAP-55; post-v1 integration pass).

**Deployment architecture:**
- Path-conditional deployment for GAP-4 Path A (LangGraph), Path B (SDK), Path C (Hybrid), incorporating GAP-56 burst-limit density validation, GAP-57 per-operator binary distribution, GAP-58 state-machine completeness per path (OQ-PATH-DEPLOY).

---

═══════════════════════════════════════════════════
# PART VI — CROSS-CUTTING PROTOCOLS (v1.2 Additions)
═══════════════════════════════════════════════════

