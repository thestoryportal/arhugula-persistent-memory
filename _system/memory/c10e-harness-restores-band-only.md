---
name: c10e-harness-restores-band-only
description: C10 harness snap_layers/restore_layers (c10e_bandknob.py:150–158) cover only hp.layers; out-of-band writers must snapshot+hash every layer they touch.
metadata:
  type: project
---

Found 2026-10-07 by the ASTRA (D-C10z-astra) prereg drafter and verified by reading the code: `snap_layers(hp)` clones `npd[weight_name(hp, layer)] for layer in hp.layers`; `restore_layers` writes back the same set. Fine for band-confined writers (step 4's maps stay inside layers 4–8, checked by its implementation review).

**Why:** a late-layer writer (ASTRA's carrier-selected layers, a per-layer DOW-KE update) would silently contaminate every later arm in the same process.

**How to apply:** any new driver whose writes can leave `hp.layers` must snapshot/restore/hash all 36 `down_proj` weights (restore in `finally`, and assert no capture hooks remain before evaluation); reviewers should check this explicitly. Related: CORPUS/61 (ASTRA).
