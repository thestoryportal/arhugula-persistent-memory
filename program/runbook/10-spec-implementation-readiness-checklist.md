## §10 — SPEC IMPLEMENTATION-READINESS CHECKLIST
═══════════════════════════════════════════════════════════════════════
_Each maps experiment(s) → spec contract. Mark as evidence lands._
- [ ] Cross-entity isolation at scale holds OR a hybrid read-path is specified — **A2/A3/A5** → §8.2/D20, §7.3
- [~] Capacity law — **DIRECTIONAL DONE (D-D1-1, `evidence/CORPUS/22`):** global total-edge-count INSUFFICIENT; §8.7 drift must be relation-concentration-aware (two-variable). Quantitative thresholds/size-term PENDING (high-cardinality replication + B1) — **D1** → OQ-W1/§8.7, §22
- [ ] C15 band reconciled for small models (keep / recalibrate) — **A4** → §8.2 C15, OQ-W2
- [ ] Genesis batch write is locality-safe at scale — **A1** → §7.7
- [ ] Multi-token value fidelity bounded/known — **C2** → value model
- [ ] Real Q4_K survival + overlay size CPU-feasible — **B3/B2** → deployment
- [ ] CPU serving of the validated store confirmed — **E1** → D1/G5
- [ ] Governance (2PC/ledger/security/validation) — **CP1–G3 DONE** → §9/§10/§11/§20/§46
- [ ] All findings reconciled into spec amendments + readiness verdict — **F1**

═══════════════════════════════════════════════════════════════════════
