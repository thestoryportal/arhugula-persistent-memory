# models

**Job:** Holds model payloads, one folder per model: `models/<model-name>/`. Edited payloads are in `variants/<variant>/<format>/`. Provenance is in `manifests/`. Weight bytes are ignored by Git. The manifests and guides are tracked.
**Read it when:** You load, serve or convert an edited model, or you place a new model payload. Read `_system/governance/STORAGE.md` § Models first.
**Written by:** The root tidy of 2026-10-23 (`program/migrations/root-tidy-20261023/`). A new payload is placed by STORAGE.md § Models.
**Read by:** `models/Qwen_Qwen2.5-3B/CONTEXT.md` names the readers of each variant.
**Not here:** Base weights in the HF cache layout: `data/CONTEXT.md` (`hf_cache`). Covariance statistics: `data/CONTEXT.md`. Run outputs: `experiments/CONTEXT.md`.
