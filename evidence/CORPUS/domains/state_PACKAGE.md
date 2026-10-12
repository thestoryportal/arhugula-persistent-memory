# PACKAGE — ⚖️ State Consistency Theorist
_Run under COUNCIL_PROTOCOL.md. Audit vs CORPUS 05 §State. Concern: do Git + .vindex agree; what's the state if power fails mid-write._

## Your spec contract (audit baseline)
Two mediums (Git + `.vindex`) must agree; **2PC + Transaction Controller**; **State Ledger maps Git commit ↔ .vindex snapshot (Merkle-chain)**; circuit breaker → READ_ONLY on trip; tiered `.vindex` for independent rollback (§8.4); ANCHOR events reset drift (§8.7); Pruning Agent; COMPACTION_REGRESSION (prior facts survive recompile).

## Relevant evidence (cite from 01)
- L-ROLL: rollback by serving the frozen base alone (file-level) → original restored. Base unmodified.
- L-BRIDGE: edit lives in a SEPARABLE `.vlp` overlay on the frozen base (tier-stack-like).
- T2.5 / A5: COMPACTION_REGRESSION analog — incremental 100% → compacted 100% (facts survive recompile). ✅ this one maps directly.
- T2.6: layer-band tiering does NOT isolate; tiers should share band w/ shared preserve state (relevant to tier-stack design).

## Standing questions to adversarially answer (governance core — partial)
1. **2PC / State Ledger (G1 — likely BLOCKER for spec)**: we have NO Git↔.vindex 2PC, NO State Ledger, NO Transaction Controller, NO circuit breaker. Our "rollback" is file-level (serve base / drop overlay), NOT ledger-coordinated. Is file-level rollback a sufficient primitive ON WHICH the 2PC/Ledger can be built, or a different model?
2. **Atomicity / power-fail**: `COMPILE` writes a new vindex (we saw `.tmp.<pid>` → rename). Is the compile atomic? What's the state if it dies mid-COMPILE? (UNTESTED.)
3. **COMPACTION_REGRESSION**: ✅ our T2.5/A5 evidence satisfies "prior facts survive recompile" — VERIFY this maps to the spec's named probe.
4. **Authoritative medium + concurrency**: which medium wins on divergence; concurrent-write sequencing — UNTESTED.

## Seeded gap: G1 (2PC/State-Ledger/TC/circuit-breaker entirely UNTESTED). Confirm; assess whether the bridge's file-level frozen-base+overlay is a sound FOUNDATION for the 2PC/Ledger (it likely is — overlay/base separation is exactly what a ledger snapshots), and whether building 2PC is local/orchestration work (DEFER-TO-LOCAL) vs a viability BLOCKER.
