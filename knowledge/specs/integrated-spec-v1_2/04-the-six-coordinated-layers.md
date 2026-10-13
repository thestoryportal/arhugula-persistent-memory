## 3. The Six Coordinated Layers

| Layer | Primary Concern | Key Components |
|---|---|---|
| Schema | What the graph can represent | Entity taxonomy, relation families, Genesis tiers |
| Write Engine | How facts enter model weights | MEMIT, `.vindex` overlays, `.larql` patches, drift tracking |
| Validation | Whether outputs are correct before commit | Reflexion loop, TGA cascade, Meta-Validator |
| Security | Who is authorized to write and how | Gate, tokens, Write Scope Definitions, audit trail |
| State Consistency | Whether both mediums agree | 2PC, Transaction Controller, Pruning Agent, Ledger |
| Orchestration | How all components are coordinated | Orchestrator, review queues, lock/hold registry |

**v1.2 cross-cutting additions (Part VI):** Eight protocols cut across multiple layers — Ceremony Authorization (§20), L2 Probe Family (§21), `larql_fidelity_calibration` (§22), CAK Bootstrap / Burst / Break-Glass (§23), Corpus Author Expiry (§24), Q5 Weak-Check (§25), External Document Provenance (§26), and Ledger Retention (§27). These are first-class spec content, not addenda. Layer sections cross-reference them where relevant.

---

═══════════════════════════════════════════════════
# PART II — TRUST BOUNDARY SCOPE
═══════════════════════════════════════════════════

