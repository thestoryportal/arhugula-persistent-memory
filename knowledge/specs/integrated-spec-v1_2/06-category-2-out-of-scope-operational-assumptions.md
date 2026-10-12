## 5. Category 2: Out-of-Scope Operational Assumptions

- Physical security of the host machine.
- Integrity of the base model file at installation (operator responsibility).
- Network security for external content ingestion (operator-controlled).
- Notification infrastructure for integrity violations (OQ-S8 — deployment-specific).
- Backup strategy for `<harness_root>/` (operator responsibility).
- Physical-access provision for break-glass CAK rotation (C-BG-4; operator pre-arranges custodians; see Appendix A).
- `.dry-run-store/` content-level immutability before executor signing (T-S-RP-1 accepted for v1; metadata-only Warden audit per IC-DRS-1; content-addressed storage v2-flagged).
- Worst-case legitimate Genesis event-count modeling against the N=5/10min burst limit (GAP-56 — empirical validation scoped to pre-ship).
- Operator workflow for break-glass custodian pre-arrangement (T-W-BG-1 accepted design tradeoff; deliberate friction is the security property).

