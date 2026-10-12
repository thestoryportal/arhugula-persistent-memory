## 6. Category 3: Deferred to v2

- Full PKI: mass revocation lists, Orchestrator key rotation, multi-Orchestrator trust.
- OOK and CAK key rotation ceremonies with full dependency map (GAP-19).
- Delegation tokens for nested sub-agent invocations (Path B/C nested cases).
- Pre-receive Git hooks (prevent-at-write for Tier 3 config).
- Multi-machine harness with Ledger replication and distributed consensus (GAP-18).
- Voluntary Write Lock release and inter-agent negotiation (GAP-17, OQ-CW1).
- Genesis automation proxy (secondary LLM reviewer as human-review substitute, GAP-13). Human review remains mandatory in v1.2.
- Genesis security model for fully automated pipelines (OQ-S5).
- Peer agent review delegation token design (GAP-20 — agent-to-agent trust model).
- `.larql` schema version migration path authorship and deprecation ceremony (OQ-W6 residual).
- T15 m-of-n CAK availability path (OQ-S-CAK-2; break-glass per §23.3 partially addresses OQ-S-CAK-1 for v1.2).
- T16 ceremony-scope narrowness: batch Genesis Hold release and multi-Hold ceremony scoping.
- Batch Genesis Hold release ceremony (T16 outline — per-Hold model remains v1.2 path).
- GAP-32 further scope-update rate-limit policy evolution.
- Sampled-verification for Ledger chains exceeding 10M entries (GAP-59 — design deferred per GAP-53 documentation threshold).
- Retired-key revocation metadata semantics: retired-clean vs. retired-compromised classification for archive-bundle signing keys (GAP-60 — per GAP-52 open question).
- Empirical threshold calibration outputs: drift thresholds, MEMIT sub-batch ceiling, ε coefficient, M in T13 three-tier model (GAP-1, GAP-2; protocol structure in §22 is ratified, numeric outputs are implementation-phase).
- Stale Layer 4 fact reconciliation workflow (OQ-SC3 — implementation-time decision per v3 GS13 disposition).
- TGA split into TGA-Test / TGA-Probe (T-TGA-load v2-reconsider flag; activates only if v1.2 operation surfaces concrete failure-mode evidence).
- Path-conditional deployment architecture for GAP-4 Path A (LangGraph), Path B (SDK), Path C (Hybrid) — activates on operator selection of a path (GAP-56/57/58 preconditions).
- Aggregate-detection entry type convention (GAP-55 — formal framework convention for always-SECURITY category, `source_entry_hash_list` field, cross-linked review queue item; post-v1 integration pass).

---

═══════════════════════════════════════════════════
# PART III — THE SIX LAYERS
═══════════════════════════════════════════════════

