## §9 — MASTER DECISION-TREE MAP
═══════════════════════════════════════════════════════════════════════
```
A0 (DONE: cross-entity FAIL) ─► A1 (batch?) ──┬─ helps ──► fold batch in
                                              └─ no ─────► (expected)
                              ─► A2 (in-solve sentinels) ─┬─ PASS ───► B1 ─► B2/B3 ─► E1 ─► F1   [in-weight fix wins]
                                                          ├─ PARTIAL ► A3 (BetaEdit) ± A4 (band) ─┬─ PASS ► B1…►F1
                                                          │                                       └─ no ─► A5
                                                          └─ FAIL ───► A5 (WISE hybrid) ─┬─ PASS ► hybrid recipe ► E1 ► F1
                                                                                         └─ no ─► A6 (SAE frontier) ─┬─ PASS ► novel fix ► F1
                                                                                                                     └─ FAIL ► spec: in-weight cross-entity ceiling = X; mandate hybrid (F1)
A4 (band) feeds C15 spec note + OQ-W2 regardless.
Track C (multi-token) runs in parallel; Track D (capacity law) starts after first A-signal and is REQUIRED for F1.
Any branch's result → update §0.3, §12, §13, CORPUS, memory.
```
**Invariant:** every fork is selected by *pre-registered empirical thresholds* (§7.4), not by preference. Ambiguous data → `advisor()` before branching.

═══════════════════════════════════════════════════════════════════════
