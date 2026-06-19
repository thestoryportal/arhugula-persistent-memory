---
name: easyedit-assets-vendored
description: "EasyEdit editor/dataset assets vendored into the workspace, mapped to the escape-hatch rungs"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

EasyEdit (github.com/zjunlp/EasyEdit) is vendored for the Write-Engine Viability program (2026-06-17):
- Full shallow clone: `/workspace/easyedit_upstream`
- Organized parts bin: **`/workspace/easyedit_assets/`** (symlinks; read its `README.md` first)

Rung map (plan `write_engine_viability_determination_plan.md`):
- `rung2b_wise/` — WISE overlay-subspace sharding (≈ `.vindex` tiers)
- `rung3_alphaedit/` — AlphaEdit null-space projection; OUR novel step = build P from the entity's OWN other (s,r') keys (entity-aware), then isolate (LAW #5)
- `rung5_grace/` — GRACE parameter-preserving existence proof (also have `/workspace/grace_dry_run/`)
- `reference_memit_rome/`, `parameter_preserving/` (serac/melo/mend), `datasets/` (counterfact/zsre/MQuAKE/knowedit), `evaluate/`
- All three rung editors have gpt-j-6B AND qwen2.5-7b hparams.

USAGE RULES (load-bearing):
- Parts bin behind our gates, NOT a replacement. Phases 0–2 keep OUR pinned engine `/workspace/memit_dry_run/memit` (fingerprint `5c0c706a…c78770`, `_cov_cpu==3`, P-VRAM-CPU-SOLVE — EasyEdit MEMIT likely OOMs Qwen on the 24GB 4090). Adopt EasyEdit editors only at Phases 3–5, under LAW #5 isolation.
- EasyEdit `evaluate/` "locality" is CROSS-ENTITY (the blind spot the program corrects) — keep our same-entity JS metric ([[memit-cov-inversion-not-a-hang]] is unrelated; the metric lives in s242_gatecal.py).
- RippleEdits is NOT bundled (no loader) — acquire separately (github.com/edenbiran/RippleEdits) for external same-entity validation.

Durable session state: `/workspace/SESSION_CHECKPOINT.md`.
