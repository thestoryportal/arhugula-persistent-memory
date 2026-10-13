## §11 — RISK REGISTER (result-invalidators + mitigations)
═══════════════════════════════════════════════════════════════════════
| Risk | Mitigation |
|---|---|
| **False-no-op** (unexpressed edit inflates locality) | Always measure apply-time expression separately (§7.4); expression gate. |
| **Tautology via overlapping pools** | 3 disjoint pools, asserted in code (A2). |
| **Metric mismatch** (JS ≠ top-1 claim) | Track top-1 AND margin AND KL; verdicts on the metric that matches the claim. |
| **Anchor-tuned thresholds** | Pre-register from DB-viability, not observed output (§2.3). |
| **GPU FP non-determinism** | Bit-repro is a non-requirement; verify behaviorally; report which-records-vary as noise. |
| **Disk exhaustion mid-run** | Pre-flight reclaim (§3.3) before downloads; durable outputs only to /workspace. |
| **Engine drift from a shim** | LAW#5 inertness gate every run (§2.4); λ_s=0 / empty-P controls. |
| **Same-model confirmation bias** | Independence discipline; advisor; empirical-only binding (§2.5). |
| **Over-investing in a frontier bet** | Gate A6 strictly on A2/A3 first. |

═══════════════════════════════════════════════════════════════════════
