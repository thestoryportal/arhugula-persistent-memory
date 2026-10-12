# Reproducibility

This document lets an independent researcher re-run any experiment and trace any claim to its raw artifact. It implements the **ML Reproducibility Checklist** (code + data + exact commands + environment + seeds + reporting of variation) and **FAIR** access norms. The authoritative per-experiment provenance is `evidence/CORPUS/01_PROVENANCE_MANIFEST.md` and `program/registers/EXPERIMENT_REGISTRY.md`; environment detail is `evidence/CORPUS/04_ENV_AND_DEPS.md`.

## Environment
- **Hardware:** RunPod, single NVIDIA RTX 4090 (24 GB). `/workspace` is a MooseFS network volume; large infra is never moved (see path convention). Deployment target is the operator's **Intel CPU** (edit-time = GPU/offline, inference-time = CPU).
- **SUPERSEDED 2026-10-03 (D-HW-1):** the RunPod volume was lost. Science hardware **and** deployment target = the operator's MacBook M3 Pro (48 GB unified memory, Apple MPS, no CUDA); `LLMDB_ROOT` = the clone root; environment pinned in `pyproject.toml` (uv). Results above this line were produced on the 4090; any re-run here must pass the LAW#3 known-baseline gate first. MPS has no float64, so the CPU-side float64 solve (the vendored CPU-solve patch) is a requirement, not a mitigation.
- **Python / ML stack:** `transformers==4.51.0` (PINNED — 4.45 lacks Qwen3, 5.x breaks the engine nethook), PyTorch + CUDA, `torch.float16` model loads. Qwen3-only work used transformers 5.12.1 in an isolated context where noted.
- **Editing engine:** `code/memit/vendor` — the `kmeng01/memit` reference fork, **UNMODIFIED on the science path** (LAW#5: any harness-side reimplementation must first prove bit-for-behavior reproduction on a null edit — the "inertness gate"). Scripts `sys.path.insert` + `os.chdir` to `${LLMDB_ROOT}/code/memit/vendor`. **Vendored in-repo since 2026-10-03** (the RunPod volume was lost): upstream `80426fd9` + P-1..P-7 (`code/memit/provenance/memit-patches-canonical.md`) + the S2.31 CPU-solve patch **+ P-8 device neutrality (2026-10-03, D-HW-1; `code/memit/provenance/memit-patches-canonical.md` §3.9)**; only its downloaded `data/` stats are gitignored. `python3 code/memit/engine_fingerprint.py` is the LAW#1 gate.
- **Deployment toolchain:** self-built `code/vendor/llama_cpp_src/` (CPU build) for real Q4_K_M GGUF quantize/serve; `code/vendor/external_prior_art/larql/target/release/larql` for vindex ingest (CPU-only on NVIDIA — no CUDA backend).
- **Caches:** `data/hf_cache/` (HF models; `HF_HOME`), `data/covariance/` (precomputed MEMIT second-moment statistics per model/band — expensive, reused).

## Path convention (`LLMDB_ROOT`)
After the 2026-06-18 reorganization, live scripts resolve paths against a repo root:
```python
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
os.environ.setdefault("HF_HOME", f"{LLMDB_ROOT}/data/hf_cache")
ENGINE_ROOT = f"{LLMDB_ROOT}/code/memit/vendor"
sys.path.insert(0, ENGINE_ROOT); os.chdir(ENGINE_ROOT)
```
`export LLMDB_ROOT=/path/to/repo` to run from a different location. `.sh` scripts use `$LLMDB_ROOT`. **Frozen `archive/` scripts (s-series, historical) were NOT rewritten** — they target the original flat `/workspace` layout and are kept for provenance, not re-execution.

## Determinism & seeds
- MEMIT edits are deterministic given fixed model revision + cached covariance + hyperparameters; the **inertness gate** (`|Δexpr|≈0`) checks the harness reproduces the reference engine bit-for-behavior before each run.
- **Cross-process bit-exact weight reproduction does NOT hold** (GPU floating-point); this is a documented non-requirement — verification is behavioral (top-1 / distributional), not by weight hash.
- Most runs are **single-seed** (stated as a caveat in each CORPUS doc). Where multiple seeds were used (A2b: 3 seeds), it is noted. Report variation honestly; do not average over a confound (see `[[match-metric-to-the-claim]]`).

## Per-experiment re-run table
`LLMDB_ROOT` assumed exported. Pre-registered pass criteria live in each `evidence/CORPUS/NN` doc and `G6_G7_PASS_CRITERIA_DRAFT.md` (now `docs/`).

| ID | command | needs GPU? | expected artifact |
|---|---|---|---|
| **G6.1** scale-of-N | `python code/lab/scale/g6_scale_n.py` (env `WRITE_MODE=sequential`) | yes | `experiments/g6/runs/g6_scale_n/g6_scale_n_result.json` |
| **A1** batch vs seq | `WRITE_MODE=batch python code/lab/scale/g6_scale_n.py` | yes | `experiments/g6/runs/g6_scale_n_batch/g6_scale_n_batch_result.json` |
| **A2** sentinels | `python code/lab/track_a/a2_relbal_sentinels.py` | yes | `experiments/a2/runs/a2_relbal_sentinels/a2_relbal_sentinels_result.json` |
| **A2b** K_S refresh | `python code/lab/track_a/a2b_refresh_ks.py` | yes | `experiments/a2b/runs/a2b_refresh_ks/a2b_refresh_ks_result.json` |
| **B1** size-density (7B) | `MODEL_ID=Qwen/Qwen2.5-7B HPARAMS=…/configs/hparams/qwen25_7b_memit_hparams.json SCREEN=…/configs/screens/g6_screen_qwen7b.json WRITE_MODE=batch RESULT_TAG=_qwen7b python code/lab/scale/g6_scale_n_param.py` | yes | `experiments/g6/runs/g6_scale_n_batch/g6_scale_n_batch_result_qwen7b.json` |
| **B3** quant survival | `bash code/lab/track_b/b3_run.sh` (convert→Q4_K_M→probe→verdict) | yes (+CPU serve) | `experiments/b3/runs/b3_quant_survival/b3_quant_survival_result.json` |
| **B3** verdict only | `python code/lab/track_b/b3_verdict.py` | no | recomputes the PASS from `results/b3_pred_*.json` |
| **E1** LARQL serve | `larql convert gguf-to-vindex --level inference b3_edited_q4km.gguf …` then `larql lql 'USE …; INFER …'` (see `evidence/CORPUS/18`) | no (CPU) | `experiments/e1/runs/e1_larql_serve/e1_larql_serve_result.json` |
| **A7** bias ablation | `python code/lab/track_a/a7_bias_ablation.py` | yes | `logs/a7_bias_ablation.log` |
| **C2** keying probe | `python code/lab/track_c/c2_key_collinearity.py` | yes | `experiments/c2/runs/c2/c2_result.json` |
| **C2b** depth map | `python code/lab/track_c/c2b_depth_map.py` | yes | `experiments/c2b/runs/c2b_depth_map/c2b_depth_map_result.json` |
| **C2-band** falsifier | `python code/lab/track_c/band_corruption_compare.py` (band [8-12] vs [4-8], seq N=100) | yes (+cov L9-12) | evidence/CORPUS/21 |
| **D1** capacity law | `python code/lab/track_d/d1_predictor_map.py` ; `d1_concentration_sweep.py` ; `d1_dose_response.py` | yes | `experiments/d1/runs/d1_predictor_map/d1_predictor_map_result.json`, `results/d1_concentration_sweep_*`, `experiments/d1/runs/d1_dose_response/d1_dose_response_result.json` (evidence/CORPUS/22) |
| **B1** size-term (3B vs 7B) | `python code/lab/track_b/b1_size_dose_response.py` (matched-harness dose-response; 7B VRAM adaptations) | yes | `results/b1_{3b,7b}_dose_response_result.json` (+`_seeds123`/`_seeds345`) (evidence/CORPUS/22 §B1) |
| **D1-2** §8.7 threshold instrument | `python code/lab/track_d/d1_threshold_instrument.py` (MODE lowk / mixedload; determinism env) | yes | `experiments/d1/runs/d1_threshold_lowk_3b_s2/d1_threshold_lowk_3b_s2.json`, `experiments/d1/runs/d1_mixedload_smoke_3b_s3/d1_mixedload_smoke_3b_s3.json` (evidence/CORPUS/22) |
| **CP1–G3** governance | `python code/lab/governance/{cp1_governed_write,g1_two_phase_commit,g2_security_layer,g3_validation_pipeline}.py` | CP1 yes; G1–G3 no | `results/*_result.json`, `results/*_state_ledger.jsonl` |
| **B3N** in-weight-necessity | *analysis decision — no runner* | no | `knowledge/findings/B3_IN_WEIGHT_NECESSITY_DECISION.md` (reasoned position, not an empirical PASS) |
| D-C10z-v7diag ⟨D-C10z-v7diag@d8c55e7b⟩ — DONE/A1 | Recorded code/lab/runners/run_c10z_v7_diag.py (one-shot; no repeat authority) | recorded GPU | experiments/c10z/runs/c10z_v7_diagnostic/20261009T182427Z/verdict.json → evidence/CORPUS/59_C10Z_V7DIAG_A1.md |
| D-C10z-a1pop ⟨D-C10z-a1pop@1ef441d3⟩ — ADMITTED preparation; continuation CLOSED under D-C10z-a4 ⟨D-C10z-a4@e0a21d13⟩ | Recorded code/lab/track_c/c10z_astra_benchmark.py; historical admission; new experimental work requires prospective authorization | recorded benchmark GPU | experiments/c10z/runs/c10z_astra_benchmark/20261009T202713Z_drift3_a1/benchmark.json → evidence/CORPUS/59_C10Z_V7DIAG_A1.md |
| D-C10z-a4 ⟨D-C10z-a4@e0a21d13⟩ — terminal stage-1 UNDERFIT | Model-free reader only: LLMDB_ROOT=<worktree> .venv/bin/python -B code/lab/track_c/c10z_astra_read.py experiments/c10z/runs/c10z_astra_attempt4; no experiment retry authorized | CPU metadata reader | experiments/c10z/runs/c10z_astra_attempt4/pass_p1.json → evidence/CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md |
| D-ML-1 ⟨D-ML-1@46230e48⟩ — STOPPED; calibration FAIL | Recorded code/apps/mathlab/run_mathlab_cpu.sh with code/apps/mathlab/m3_calibration.py; harvest-2 bindings preserved; no rerun authorized | recorded CPU calibration | experiments/ml/runs/m3_20261009T225557.353172Z/calibration.json → evidence/CORPUS/60_MATHLAB_HARVEST_REPLAY.md#2026-10-09-addendum--harvest-2-calibration-fail-lab-stopped-d-ml-1--d-ml-4 |
| D-ML-4 ⟨D-ML-4@46230e48⟩ — lab stop; step 4 SHELVED | Stop disposition only; step-4 draft NOT FROZEN/NOT RUN; future proxies need written amendment/unused-arm calibration | no new run | experiments/ml/reviews/m3_reading_astra.md → evidence/CORPUS/60_MATHLAB_HARVEST_REPLAY.md#2026-10-09-addendum--harvest-2-calibration-fail-lab-stopped-d-ml-1--d-ml-4 |
| D-ML-2 ⟨D-ML-2@99a9fb4c⟩ — Bounded harvest-1 replay PASS/OPERANDS-ONLY | Recorded code/apps/mathlab/run_mathlab_cpu.sh with code/apps/mathlab/m2_solve_repro.py; frozen historical pins | CPU | experiments/ml/runs/m2_20261009T192823.926873Z/manifest.json → evidence/CORPUS/60_MATHLAB_HARVEST_REPLAY.md |
| D-ML-3 ⟨D-ML-3@84e9d0e1⟩ — NORM-CONTRACT implemented; fresh admission recorded | Recorded code/apps/mathlab/run_mathlab_harvest.sh under the frozen native norm contract | recorded GPU harvest | experiments/ml/runs/harvest_20261009T203705.724371Z/manifest.json → evidence/CORPUS/60_MATHLAB_HARVEST_REPLAY.md |

> **Keep-current note (2026-06-21):** this re-run table is now part of the experiment close-out set (`_system/governance/DISCIPLINE.md` §1.1) — add a row when a new experiment lands, so it stops silently falling behind (it had drifted to ~C2 before this). The durable env / path / determinism sections above are stable; only this table + the seeds note need per-experiment upkeep. **Determinism path for the lower-variance instrument:** `torch.use_deterministic_algorithms(True)` + `CUBLAS_WORKSPACE_CONFIG=:4096:8` + `ATTN=eager` (byte-reproducible across processes on 3B; binding 3B uncertainty is edit-ORDER — `[[sequential-edit-run-nondeterminism]]`).

## Tracing a claim to its artifact
1. Find the claim in `evidence/CORPUS/NN_*.md` (or the headline table in `README.md`).
2. Its header lists `Artifacts:` (scripts + result JSON + logs) and a `Decision-ID` (`D-<TRACK><n>`).
3. Resolve a basename to its path via `program/registers/EXPERIMENT_REGISTRY.md` or `find . -name <basename>`.
4. `evidence/CORPUS/01_PROVENANCE_MANIFEST.md` maps claim → {script, result file, exact numbers}; `evidence/CORPUS/02_VANDV_CHAIN.md` gives hypothesis → method → measurement → criterion → verdict.

## Rollback / integrity
Pre-reorganization snapshot (2026-06-18) at `/root/migration_backup/`: `manifest_pre.tsv` (all paths/sizes/mtimes), `hashes_pre.txt` (md5 of small text files), `small_files_pre.tgz` (full text-file backup), `migration_map.tsv` (old→new mapping, reversible). Infra dirs were never moved.

| **C10 band-knob** | `python code/lab/track_c/c10e_bandknob.py` | yes (+cov L9-12 if absent) | `experiments/c10e/runs/c10e_bandknob/c10e_bandknob.json` (evidence/CORPUS/37; D-C10e-bandknob ⟨D-C10e-bandknob@82b491dc⟩) |

| **C10 widened [4,12]** | `python code/lab/track_c/c10f_band412.py` | yes (+cov L9-12 if absent) | `experiments/c10f/runs/c10f_band412/c10f_band412.json` (evidence/CORPUS/38; D-C10f-band412 ⟨D-C10f-band412@d93d6a19⟩) |

| **C10 strength/layer sweep** | `python code/lab/track_c/c10g_strength_layer_sweep.py` | yes (+cached cov L4-12,18-22 if absent) | `experiments/c10g/runs/c10g_strength_layer_sweep/c10g_strength_layer_sweep.json` (evidence/CORPUS/39; D-C10g-strengthlayers ⟨D-C10g-strengthlayers@d691acab⟩) |

| **C10 AnyEdit small-window pilot** | `python code/lab/track_c/c10h_anyedit_pilot.py --dry-run` then `python code/lab/track_c/c10h_anyedit_pilot.py` | yes | `results/c10h_anyedit_token_window_dryrun.json`; `experiments/c10h/runs/c10h_anyedit_pilot/c10h_anyedit_pilot.json` (evidence/CORPUS/40; D-C10h-anyedit-pilot ⟨D-C10h-anyedit-pilot@6413cc67⟩) |

| **LAW#3 repro (M3 Pro)** | `python code/lab/track_c/c2_key_collinearity.py` ; `WRITE_MODE=batch python code/lab/scale/g6_scale_n.py` | yes (MPS) | `experiments/law3-repro/runs/law3_repro_2026-10-03/{c2_key_collinearity_repro,a1_batch_repro}.json` (2026-10-04; D-HW-1) |

| **LAW#5 inertness gate** | `python code/gates/law5_inertness_gate.py --out <path>` | yes (MPS) | `experiments/law3-repro/runs/law3_repro_2026-10-03/law5_inertness_p8.json` |

| **B3 local serving (M3 Pro)** | `python code/lab/track_b/b3_edit_and_save.py` ; `python code/lab/track_b/b3_expand_native.py` ; `bash code/lab/track_b/b3_run.sh` (prebuilt llama.cpp at `code/vendor/llama_cpp_src/build/bin`) | yes (MPS edit) + CPU serve | `experiments/law3-repro/runs/law3_repro_2026-10-03/b3/b3_repro.json` (2026-10-04) |

| **C10L solve geometry / sparse sets (M3 Pro)** | `C10_PROJECTOR=identity CANDIDATE_NAME=armB_identity HP_CANDIDATE=code/configs/hparams/qwen25_3b_memit_hparams.json python code/lab/track_c/c10e_bandknob.py` ; `HP_CANDIDATE=…_set48.json` / `…_set78.json` ; `python code/lab/track_c/c10l_covgeom_p6_zinject.py` ; `python code/lab/track_c/c10l_covgeom_step0.py` ; read with `c10l_covgeom_read.py` | yes (MPS) | `experiments/c10l/runs/c10l_covgeom/` (evidence/CORPUS/44; D-C10l-covgeom ⟨D-C10l-covgeom@af2e38f7⟩) |

| **C10L minted token (M3 Pro)** | `python code/lab/track_c/c10l_mint_step0.py` ; `MINT_ARM=multi\|rare\|G\|N LAW3_REF=<covgeom run JSON> python code/lab/track_c/c10l_mint_arms.py` ; read with `c10l_mint_read.py`; B2/B3: `MINT_INITS=N MINT_N_SEED=1 MINT_INIT_TAG=_seed1 OUT=experiments/c10l/runs/c10l_mint/step0_probe_seed1.json python code/lab/track_c/c10l_mint_step0.py`, `MINT_ARM=N MINT_SAVE_DIR=<dir> python code/lab/track_c/c10l_mint_arms.py`, `bash _archive/code/closed-runners/c10l_mint_p4.sh`, read with `c10l_mint_b3_read.py experiments/c10l/runs/c10l_mint experiments/c10l/runs/c10l_mint/p4_verdict.json` | yes (MPS) | `experiments/c10l/runs/c10l_mint/` (evidence/CORPUS/45; D-C10l-mint ⟨D-C10l-mint@a4a6f4c7⟩) |
| **C10M diagnostics (M3 Pro)** | `LAW3_REF=<covgeom run JSON> OUT=experiments/c10m/runs/c10m_diag/diag_run2.json python code/lab/track_c/c10m_diag_arms.py` ; third seed via `MINT_INITS=N MINT_N_SEED=2 MINT_INIT_TAG=_seed2 python code/lab/track_c/c10l_mint_step0.py` + `MINT_ARM=N MINT_STEP0=experiments/c10l/runs/c10l_mint/step0_probe_seed2.json python code/lab/track_c/c10l_mint_arms.py` ; read with `c10m_diag_read.py experiments/c10m/runs/c10m_diag/diag_run2.json experiments/c10l/runs/c10l_mint` | yes (MPS) | `experiments/c10m/runs/c10m_diag/` (evidence/CORPUS/46; D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩) |
| **C10N target transport (M3 Pro)** | `LAW3_REF=<covgeom run JSON> python code/lab/track_c/c10n_ztransport_arms.py` (OUT defaults to experiments/c10n/runs/c10n_ztransport/run.json) ; read with `c10n_ztransport_read.py experiments/c10n/runs/c10n_ztransport/run.json` | yes (MPS) | `experiments/c10n/runs/c10n_ztransport/` (evidence/CORPUS/47; D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩) |
| **C10O magnitude/direction (M3 Pro)** | `LAW3_REF=<covgeom run JSON> python code/lab/track_c/c10o_magnitude_arms.py` (OUT defaults to experiments/c10o/runs/c10o_magnitude/run.json) ; read with `c10o_magnitude_read.py experiments/c10o/runs/c10o_magnitude/run.json` | yes (MPS) | `experiments/c10o/runs/c10o_magnitude/` (evidence/CORPUS/48; D-C10o-magnitude ⟨D-C10o-magnitude@31389765⟩) |
| **C10P two-pass solve (M3 Pro)** | `LAW3_REF=<covgeom run JSON> python code/lab/track_c/c10p_twopass_arms.py` (three passes; outputs under experiments/c10p/runs/c10p_twopass/) ; read with `c10p_twopass_read.py experiments/c10p/runs/c10p_twopass` | yes (MPS) | `experiments/c10p/runs/c10p_twopass/` (evidence/CORPUS/49; D-C10p-twopass ⟨D-C10p-twopass@12f87dc3⟩) |
| **C10Q stacked two-pass solve (M3 Pro)** | `LAW3_REF=<covgeom run JSON> python code/lab/track_c/c10q_stacked_arms.py` (three passes S / S-sham / S-perm; outputs under experiments/c10q/runs/c10q_stacked/) ; read with `c10q_stacked_read.py experiments/c10q/runs/c10q_stacked` | yes (MPS) | `experiments/c10q/runs/c10q_stacked/` (evidence/CORPUS/50; D-C10q-stacked ⟨D-C10q-stacked@8e5c7f12⟩) |
| **C10X engine-path target construction (M3 Pro)** | `python -B code/lab/track_c/c10x_enginepath_arms.py --out <abs OUT_DIR> --go <abs go record> --process 1` (absolute paths required; a re-run adds `--predecessor <abs dir> --cause <CAUSE>`); read with `python -B code/lab/track_c/c10x_enginepath_read.py --out <abs OUT_DIR>` (exit 0 does not by itself mean VALID — read `status`) | yes (MPS) | `experiments/c10x/runs/c10x_enginepath_rerun3/` (evidence/CORPUS/58; D-C10x-enginepath ⟨D-C10x-enginepath@a8c22280⟩) |


## 2026-10-10 — Projector-fidelity warning pointer (D-NEW1-fid)

| Decision | Scope | Detailed source |
|---|---|---|
| D-NEW1-fid ⟨D-NEW1-fid@341707a8⟩ | Documentation-only closeout of existing B receipt; no numerical rerun or new reproduction command; actual projector/leakage/locality UNMEASURED | [B measurement report — D-NEW1-fid warning](results/mathlab_staging/new1_v2_build_report.md#d-new1-fid) |


## 2026-10-11 — NEW-1 one authorized execution outcome pointer (D-NEW1-c)

| Decision | Scope | Detailed source |
|---|---|---|
| D-NEW1-c ⟨D-NEW1-c@fce4a263⟩ | One authorized invocation of `code/lab/runners/new1_dispatch.sh` (endorsed command in experiments/new1/runs/new1_launch_c4_20261011/launch_manifest.md); authorization consumed, any re-run needs a new operator authorization; run dir results/mathlab_staging/runs/new1_20261010T235740.858576Z/ (finding.json, geometry.json); dispatch receipt experiments/new1/runs/new1_dispatch_20261010T235738.2180209160Z/dispatch_receipt.json | [NEW-1 outcome note](experiments/new1/runs/new1_outcome_20261011/maestro_outcome_note.md) |


⟨D-C10l-covgeom@0caeca4f⟩
