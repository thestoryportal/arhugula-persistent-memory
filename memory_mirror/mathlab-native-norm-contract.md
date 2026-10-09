---
name: mathlab-native-norm-contract
description: Compare historical norm scalars with the same write native producer return; retain analysis norms separately.
metadata:
  node_type: memory
  type: feedback
---

Historical norm consistency requires the same observed write’s native returned scalar. A higher-precision diagnostic norm is a different measurement contract and cannot substitute for that producer scalar. D-ML-1 ⟨D-ML-1@46230e48⟩ keep harvest identities separate; D-ML-2 ⟨D-ML-2@99a9fb4c⟩ replay is scoped; D-ML-3 ⟨D-ML-3@84e9d0e1⟩ compare the historical producer's native scalar → CORPUS/60_MATHLAB_HARVEST_REPLAY.md.
