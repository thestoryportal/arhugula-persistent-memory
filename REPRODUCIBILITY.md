# Reproducibility

This document lets an independent researcher re-run any experiment and trace any claim to its raw artifact. It implements the **ML Reproducibility Checklist** (code + data + exact commands + environment + seeds + reporting of variation) and **FAIR** access norms. The authoritative per-experiment provenance is `CORPUS/01_PROVENANCE_MANIFEST.md` and `docs/EXPERIMENT_REGISTRY.md`; environment detail is `CORPUS/04_ENV_AND_DEPS.md`.

## Environment
- **Hardware:** RunPod, single NVIDIA RTX 4090 (24 GB). `/workspace` is a MooseFS network volume; large infra is never moved (see path convention). Deployment target is the operator's **Intel CPU** (edit-time = GPU/offline, inference-time = CPU).
- **Python / ML stack:** `transformers==4.51.0` (PINNED — 4.45 lacks Qwen3, 5.x breaks the engine nethook), PyTorch + CUDA, `torch.float16` model loads. Qwen3-only work used transformers 5.12.1 in an isolated context where noted.
- **Editing engine:** `memit_dry_run/memit` — the `kmeng01/memit` reference fork, **UNMODIFIED on the science path** (LAW#5: any harness-side reimplementation must first prove bit-for-behavior reproduction on a null edit — the "inertness gate"). Scripts `sys.path.insert` + `os.chdir` to `${LLMDB_ROOT}/memit_dry_run/memit`.
- **Deployment toolchain:** self-built `llama_cpp_src/` (CPU build) for real Q4_K_M GGUF quantize/serve; `external_prior_art/larql/target/release/larql` for vindex ingest (CPU-only on NVIDIA — no CUDA backend).
- **Caches:** `hf_cache/` (HF models; `HF_HOME`), `covariance_caches/` (precomputed MEMIT second-moment statistics per model/band — expensive, reused).

## Path convention (`LLMDB_ROOT`)
After the 2026-06-18 reorganization, live scripts resolve paths against a repo root:
```python
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
os.environ.setdefault("HF_HOME", f"{LLMDB_ROOT}/hf_cache")
ENGINE_ROOT = f"{LLMDB_ROOT}/memit_dry_run/memit"
sys.path.insert(0, ENGINE_ROOT); os.chdir(ENGINE_ROOT)
```
`export LLMDB_ROOT=/path/to/repo` to run from a different location. `.sh` scripts use `$LLMDB_ROOT`. **Frozen `archive/` scripts (s-series, historical) were NOT rewritten** — they target the original flat `/workspace` layout and are kept for provenance, not re-execution.

## Determinism & seeds
- MEMIT edits are deterministic given fixed model revision + cached covariance + hyperparameters; the **inertness gate** (`|Δexpr|≈0`) checks the harness reproduces the reference engine bit-for-behavior before each run.
- **Cross-process bit-exact weight reproduction does NOT hold** (GPU floating-point); this is a documented non-requirement — verification is behavioral (top-1 / distributional), not by weight hash.
- Most runs are **single-seed** (stated as a caveat in each CORPUS doc). Where multiple seeds were used (A2b: 3 seeds), it is noted. Report variation honestly; do not average over a confound (see `[[match-metric-to-the-claim]]`).

## Per-experiment re-run table
`LLMDB_ROOT` assumed exported. Pre-registered pass criteria live in each `CORPUS/NN` doc and `G6_G7_PASS_CRITERIA_DRAFT.md` (now `docs/`).

| ID | command | needs GPU? | expected artifact |
|---|---|---|---|
| **G6.1** scale-of-N | `python experiments/scale/g6_scale_n.py` (env `WRITE_MODE=sequential`) | yes | `results/g6_scale_n_result.json` |
| **A1** batch vs seq | `WRITE_MODE=batch python experiments/scale/g6_scale_n.py` | yes | `results/g6_scale_n_batch_result.json` |
| **A2** sentinels | `python experiments/track_a/a2_relbal_sentinels.py` | yes | `results/a2_relbal_sentinels_result.json` |
| **A2b** K_S refresh | `python experiments/track_a/a2b_refresh_ks.py` | yes | `results/a2b_refresh_ks_result.json` |
| **B1** size-density (7B) | `MODEL_ID=Qwen/Qwen2.5-7B HPARAMS=…/configs/hparams/qwen25_7b_memit_hparams.json SCREEN=…/configs/screens/g6_screen_qwen7b.json WRITE_MODE=batch RESULT_TAG=_qwen7b python experiments/scale/g6_scale_n_param.py` | yes | `results/g6_scale_n_batch_result_qwen7b.json` |
| **B3** quant survival | `bash experiments/track_b/b3_run.sh` (convert→Q4_K_M→probe→verdict) | yes (+CPU serve) | `results/b3_quant_survival_result.json` |
| **B3** verdict only | `python experiments/track_b/b3_verdict.py` | no | recomputes the PASS from `results/b3_pred_*.json` |
| **E1** LARQL serve | `larql convert gguf-to-vindex --level inference b3_edited_q4km.gguf …` then `larql lql 'USE …; INFER …'` (see `CORPUS/18`) | no (CPU) | `results/e1_larql_serve_result.json` |
| **A7** bias ablation | `python experiments/track_a/a7_bias_ablation.py` | yes | `logs/a7_bias_ablation.log` |
| **C2** keying probe | `python experiments/track_c/c2_key_collinearity.py` | yes | `results/c2_result.json` |
| **C2b** depth map | `python experiments/track_c/c2b_depth_map.py` | yes | `results/c2b_depth_map_result.json` |
| **C2-band** falsifier | `python experiments/track_c/band_corruption_compare.py` (band [8-12] vs [4-8], seq N=100) | yes (+cov L9-12) | CORPUS/21 |
| **D1** capacity law | `python experiments/track_d/d1_predictor_map.py` ; `d1_concentration_sweep.py` ; `d1_dose_response.py` | yes | `results/d1_predictor_map_result.json`, `results/d1_concentration_sweep_*`, `results/d1_dose_response_result.json` (CORPUS/22) |
| **B1** size-term (3B vs 7B) | `python experiments/track_b/b1_size_dose_response.py` (matched-harness dose-response; 7B VRAM adaptations) | yes | `results/b1_{3b,7b}_dose_response_result.json` (+`_seeds123`/`_seeds345`) (CORPUS/22 §B1) |
| **D1-2** §8.7 threshold instrument | `python experiments/track_d/d1_threshold_instrument.py` (MODE lowk / mixedload; determinism env) | yes | `results/d1_threshold_lowk_3b_s2.json`, `results/d1_mixedload_smoke_3b_s3.json` (CORPUS/22) |
| **CP1–G3** governance | `python experiments/governance/{cp1_governed_write,g1_two_phase_commit,g2_security_layer,g3_validation_pipeline}.py` | CP1 yes; G1–G3 no | `results/*_result.json`, `results/*_state_ledger.jsonl` |
| **B3N** in-weight-necessity | *analysis decision — no runner* | no | `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md` (reasoned position, not an empirical PASS) |

> **Keep-current note (2026-06-21):** this re-run table is now part of the experiment close-out set (`DISCIPLINE.md` §1.1) — add a row when a new experiment lands, so it stops silently falling behind (it had drifted to ~C2 before this). The durable env / path / determinism sections above are stable; only this table + the seeds note need per-experiment upkeep. **Determinism path for the lower-variance instrument:** `torch.use_deterministic_algorithms(True)` + `CUBLAS_WORKSPACE_CONFIG=:4096:8` + `ATTN=eager` (byte-reproducible across processes on 3B; binding 3B uncertainty is edit-ORDER — `[[sequential-edit-run-nondeterminism]]`).

## Tracing a claim to its artifact
1. Find the claim in `CORPUS/NN_*.md` (or the headline table in `README.md`).
2. Its header lists `Artifacts:` (scripts + result JSON + logs) and a `Decision-ID` (`D-<TRACK><n>`).
3. Resolve a basename to its path via `docs/EXPERIMENT_REGISTRY.md` or `find . -name <basename>`.
4. `CORPUS/01_PROVENANCE_MANIFEST.md` maps claim → {script, result file, exact numbers}; `CORPUS/02_VANDV_CHAIN.md` gives hypothesis → method → measurement → criterion → verdict.

## Rollback / integrity
Pre-reorganization snapshot (2026-06-18) at `/root/migration_backup/`: `manifest_pre.tsv` (all paths/sizes/mtimes), `hashes_pre.txt` (md5 of small text files), `small_files_pre.tgz` (full text-file backup), `migration_map.tsv` (old→new mapping, reversible). Infra dirs were never moved.
