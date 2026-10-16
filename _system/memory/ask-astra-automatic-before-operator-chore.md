---
name: ask-astra-automatic-before-operator-chore
description: When a builder's design adds a recurring manual step for the operator, ask Astra whether an automatic equivalent exists before surfacing it as a cost
metadata:
  type: feedback
---

A builder's design can quietly hand the operator a recurring chore. R4D2's dashboard record v2 required a manual console pin on the Intel Mac after every M3 collector restart, and its report mentioned this only as a "transition tradeoff". MAESTRO42 put the question to Astra in the review packet ("AUTOMATIC TRANSITION POSSIBLE: yes/no"). Astra answered yes: a separately authenticated read-only live-state verifier gives the same guarantee. Manual pinning had been "a selected mechanism, not the technical minimum" (`knowledge/analyses/compute-storage/compute_storage_brainstorm_20261011T054507Z/astra_r4d2_verdict.md`).

**Why:** the operator's attention is scarce (operator-decision-scope). A chore that recurs on every reboot or crash is a standing cost, and builders pick the simplest safe mechanism without weighing who pays for it.

**How to apply:** when reading a builder report, look for any step a person must repeat ("operator installs", "console", "manual", "re-approve"). Add a yes/no line for it to the Astra packet. Present the reviewed alternatives, their gates and recurring manual costs to the operator before the operator chooses. Related: [[operator-decision-scope]], [[plain-language-to-operator]].
