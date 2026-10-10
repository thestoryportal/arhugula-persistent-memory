---
name: c10e-harness-restores-band-only
description: "The C10 harness's snap_layers/restore_layers (experiments/track_c/c10e_bandknob.py:149–158) snapshot and restore only hp.layers (the edit band); any arm that writes outside the band leaks into the next arm's baseline unless the driver snapshots, restores and hash-checks every layer it touches."
metadata:
  type: project
---

Found 2026-10-07 by the ASTRA (D-C10z-astra) prereg drafter and verified by reading the code: `snap_layers(hp)` clones `npd[weight_name(hp, layer)] for layer in hp.layers`; `restore_layers` writes back the same set. Fine for band-confined writers (step 4's maps stay inside layers 4–8, checked by its implementation review).

**Why:** a late-layer writer (ASTRA's carrier-selected layers, a per-layer DOW-KE update) would silently contaminate every later arm in the same process.

**How to apply:** any new driver whose writes can leave `hp.layers` must snapshot/restore/hash all 36 `down_proj` weights (restore in `finally`, and assert no capture hooks remain before evaluation); reviewers should check this explicitly. Related: [[c10k-route-a-resume]].
