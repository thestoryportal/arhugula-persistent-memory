## 4. Category 1: In-Scope Threats (Defended by Spec Mechanisms)

- Unauthorized writes to `.vindex` (Gate + token model).
- Agent overreach beyond declared Write Scope (Gate scope check).
- Prompt injection via external content (two-layer sequential defense, D38).
- Replay attacks on signed artifacts (single-use token model, Ledger consumption record).
- State divergence between Git and `.vindex` (2PC + Transaction Controller).
- Silent discard of agent failures (four-step escalation cascade, C28).
- Validator corruption or overreach (actor-critic independence, D32–D33).
- Tampered configuration artifacts (three-tier `.harness/` model, boot-time verification).
- Replay of stale `.larql` patches across schema version boundaries (C-GATE-1, IC-GATE-8).
- Unauthorized corpus authorship (C-GOC4, IC-CORPUS-AUTH; expiry enforcement §24).
- Retention policy shortening to destroy forensic evidence (C-SL2, IC-LDG-RETAIN; retention policy §27).
- Unauthorized ceremony replay or cross-ceremony token substitution (§20 unified CeremonyToken, IC-SCOPE-AUTH-1).
- Compromised operator root key at bootstrap (dual-root signing, C-BOOT-5, IC-BOOT-1, §23.1).
- CAK burst-signing attacks (per-CAK burst limit N=5/10min, `BURST_SUSPENDED`, IC-CAKB-1, §23.2).
- Primary-CAK compromise requiring rapid replacement (break-glass M≥3 quorum, `TRUST_ROOT_LOST` terminal state, IC-BG-1, §23.3).
- Low-signal scope-mismatch events aggregating into policy drift (aggregate `SCOPE_HASH_MISMATCH` detection, IC-AGG-COUNTER, §14.3).
- Stale or fabricated Layer 4 external documents (mandatory provenance block, advisory staleness, §26).
- Manifest-lattice incompleteness at ratification (IC-MANIFEST-1 Check 8).
- Pre-boot hook tampering (Tier 2 sealed `hook-registry/v1`, IC-HOOK-BOOT, `HOOK_INTEGRITY_VIOLATION`).
- Rate-limit / retention-window boot misconfiguration (`RATE_LIMIT_RETENTION_CONFLICT` boot check, IC-BOOT-RLRF).
- Genesis initiation during active Hold (`GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE`, `GENESIS_INITIATION_ABUSE_PATTERN`, IC-GIB-1).
- Genesis timeout/trip pairing failure (`GENESIS_TIMEOUT_TRIP_MISSING`, C-GTO-1/2, IC-MON-GTOTM).
- Hold-release without operator-cited precursor (`HOLD_RELEASE_REASON_UNWARRANTED`, IC-REL-PRECURSOR).
- Constitutional-invariant drift at runtime (Q5 weak-check, `CONSTITUTIONAL_FAILURE` with invariant_statement + failure_assertion_message, C-CONSTITUTIONAL-Q5, §25).

