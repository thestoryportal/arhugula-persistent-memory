---
date: 2026-06-27
source: C10i assurance-tooling discussion
scope: LLM-as-Database AutoResearch discipline
---

# AutoResearch Is Not A Faithfulness Gate

Do not use AutoResearch to decide whether an external method port is scientifically
valid. AutoResearch is an optimizer/candidate generator and is Goodhart-prone by
construction. It can search hparams or implementation variants only after the
measurement frame, held-out guard, and method-faithfulness gate are stable. Its
outputs are leads for the hypothesis register, never CORPUS evidence or promotion
claims.

For port validity, use experiment-gate + method-replication checks + advisor-review:
source-faithfulness, positive controls, active trace, metric matching, bias/confound
audit, and cross-family review. Only after that should a fenced optimizer propose
candidate improvements.
