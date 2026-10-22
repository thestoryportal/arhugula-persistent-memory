---
name: easyedit-assets-vendored
description: EasyEdit is a parts bin behind our gates, not on disk now (pod clone gone; easyedit_ref holds 2 hparam yamls); its locality is cross-entity.
metadata:
  type: reference
---

EasyEdit (github.com/zjunlp/EasyEdit) was vendored for the Write-Engine Viability program on the pod (2026-06-17: shallow clone `/workspace/easyedit_upstream`, parts bin `/workspace/easyedit_assets/` mapped to escape-hatch rungs — WISE overlay sharding, AlphaEdit null-space, GRACE, reference MEMIT/ROME, SERAC/MELO/MEND, CounterFact/zsRE/MQuAKE/KnowEdit datasets; plan/report now in `docs/write_engine_viability_determination_{plan,report}.md`). **Those pod paths are gone.** On this Mac only `/Volumes/memit/llmdb-preserved/icm21-20261013/parent/easyedit_ref/` exists, holding two hparam files (`llama-7b.yaml`, `llama3.2-3b.yaml`) — re-clone EasyEdit if an editor is needed.

USAGE RULES (load-bearing):
- Parts bin behind our gates, NOT a replacement. Keep OUR pinned engine (`memit_dry_run/memit`, fingerprint per `tools/engine_fingerprint.py`, `_cov_cpu==3`, P-VRAM-CPU-SOLVE). Adopt an EasyEdit editor only under LAW #5 isolation.
- EasyEdit `evaluate/` "locality" is CROSS-ENTITY (the blind spot the program corrects) — keep our same-entity JS metric.
- RippleEdits is NOT bundled (no loader) — acquire separately (github.com/edenbiran/RippleEdits) for external same-entity validation.
