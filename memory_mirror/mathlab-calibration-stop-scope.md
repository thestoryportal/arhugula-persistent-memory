---
name: mathlab-calibration-stop-scope
description: Keep a failed frozen proxy calibration distinct from independently gated geometry work.
metadata:
  node_type: memory
  type: feedback
---

A valid failed calibration stops the registered proxy lab and shelves its calibration-dependent next step; it does not falsify independently preregistered descriptive geometry on a different pinned harvest. NEW-1 keeps its own build/execution, calibration and prospective-utility gates. Current disposition: D-ML-1 ⟨D-ML-1@46230e48⟩ STOPPED/calibration FAIL; D-ML-4 ⟨D-ML-4@46230e48⟩ step 4 SHELVED. Full detail: `CORPUS/60_MATHLAB_HARVEST_REPLAY.md`, dated 2026-10-09 calibration-stop addendum.
