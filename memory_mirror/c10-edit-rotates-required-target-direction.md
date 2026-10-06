---
name: c10-edit-rotates-required-target-direction
description: "CORPUS/48 (D-C10o-magnitude, 2026-10-05, HIGH-CONTROL): on the C10 harness, scaling the solve's target to the re-solved norm does nothing on the edited model (5/60 vs 6/60), while the re-solved direction restores decoding (34/60 at the original norm, 47/60 with the original projection kept; re-solved target 50/60); the rotated direction is worse on the unedited model (17–23 vs 42). Routing: two-pass solve arm next."
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

The injection assay separated magnitude from direction in the target the edited model wants (CORPUS/47 found it 30 % longer and rotated). Magnitude alone recovers none of the gap; the direction carries it, and holding the original projection while adding the rotation recovers 0.93. Which four subjects keep an identical target varies per process with where the edit lands; the 0.30 displacement split separates the groups cleanly.

**Why:** it routes the next C10 mechanism arm to a harness-side, engine-untouched **two-pass solve** (edit → re-solve z on the edited model → fresh edit aimed at z_post, with a sham second edit aimed at z_pre and the locality gates fixed in the C10o prereg §3), before the engine-path arms I-1 / I-2. Routing label only — injection success does not license a weight edit's locality (CORPUS/44 F-A3).

**How to apply:** pre-register the two-pass arm with the strict held-out-paraphrase bar binding; if it fails, go solve-side (compute_z convergence, projector effect) before I-1 / I-2. See [[c10-edit-collateral-breaks-injected-target]], [[injection-control-is-a-stratum-not-a-floor]], CORPUS/46–48.
