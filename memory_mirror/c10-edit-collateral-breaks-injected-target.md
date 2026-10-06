---
name: c10-edit-collateral-breaks-injected-target
description: "CORPUS/46 (D-C10m-diag, 2026-10-05): on the C10 harness the pre-edit target that injects at 51–54/72 on the unedited model injects at only 17–23/72 once the band 4–8 edit is applied (H1 collateral bucket), while a target recomputed on the edited model injects at 55–60/72; forcing the gold first token gains 2/72 (ABSENT-dominant); injection ceilings are properties of the unedited model"
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

The pre-registered diagnostic pair that decides the C10 mechanism fork: Q1 gold-first-token-constrained read moved held-out recall 15 → 17/72 with only 3 chain-failure subjects (ABSENT-DOMINANT); Q2 edit + inject with the pre-edit z landed in the H1 (collateral) bucket (23/72, canon 7/24, against a 51/72 in-process control and 15/72 edit-only); the secondary recomputed-z injection reached 55/72, so the edited model keeps a reachable target that differs from the one the solve aimed at (hypothesis, not inference). Third minted-token N seed: 46/34/36 → SEED-SENSITIVE.

**Why:** it rules out first-token targeting and the "target is the wall" reading, and it means CORPUS/44's P6 "the target admits LEAD" ceiling is a property of the unedited model only; the next mechanism arm must change what the edit does at non-keyed positions.

**How to apply:** before I-1 OverTone / I-2 forward replay, run the cheap 2 × 2 z-transport read (z_pre / z_post × pre-/post-edit model with norms and cosines); never read an injection ceiling as the ceiling of the edited model; pre-register ≥ 3 seeds for any init comparison on the mint harness. Reader `experiments/track_c/c10m_diag_read.py`. See [[mint-replication-spread-and-gguf-survival]] and CORPUS/44–46.
