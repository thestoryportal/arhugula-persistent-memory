## 2. Architectural Summary

The harness is organized as six coordinated layers operating under a single Orchestrator-mediated control plane. A task flows through the system as follows:

```
  Human / External Input
         │
         ▼
  ┌──────────────────────────────────────────────────────────┐
  │                     ORCHESTRATOR                          │
  │   (task decomposition, agent invocation, lock/hold        │
  │    management, ledger writes, review queue routing)       │
  └──────────────────────────────────────────────────────────┘
         │                                         ▲
         │                                         │
         ▼                                         │
  ┌────────────────────┐    ┌──────────────────────────────┐
  │  TGA               │    │  Validator (+ Meta-Validator) │
  │  (test authorship) │────▶  (correctness cascade)        │
  └────────────────────┘    └──────────────────────────────┘
         │                                         │
         ▼                                         │
  ┌────────────────────┐                          │
  │  Coder Agent       │──────────────────────────┘
  │  (implementation + │         signed pass
  │   .larql drafting) │         ▼
  └────────────────────┘    ┌──────────────────────────────┐
                            │  Commit Executor              │
                            │  (sole two-medium writer)     │
                            └──────────────────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │  Patch Authorization Gate             │
                   │  (Identity → Scope → Integrity)       │
                   └───────────────────────────────────────┘
                                       │
                 ┌─────────────────────┴──────────────────┐
                 ▼                                         ▼
         ┌───────────────┐                      ┌─────────────────┐
         │  Git          │                      │  MEMIT Write    │
         │  (syntactic   │                      │  Engine         │
         │   state)      │                      │  (→ .vindex)    │
         └───────────────┘                      └─────────────────┘
                 │                                         │
                 └─────────────────┬───────────────────────┘
                                   │
                           ┌───────▼───────┐
                           │ State Ledger  │
                           │ (unified      │
                           │  integrity    │
                           │  + audit)     │
                           └───────────────┘
```

