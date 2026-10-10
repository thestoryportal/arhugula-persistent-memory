# 04 — ENVIRONMENT, TOOLCHAIN & TRAPS (reproducibility + migration input)
_What it ran on, exact versions, the traps we hit, and what's durable vs ephemeral. Feeds workstream #2 (local migration) and #3 (pre-mortem)._

## Hardware (test pod)
- RunPod: 1× RTX 4090 (24 GB), ~500 GB RAM, 446 TB network FS at `/workspace` (slow), **29 GB tmpfs at `/dev/shm` (RAM-speed)**.
- **Deployment target (operator): local Intel CPU, no GPU.** Edit-time (GPU, offline) and inference-time (CPU) are SEPARABLE.

## Software / versions (exact)
- Python 3.11, torch 2.4.1+cu124.
- **transformers: 4.51.0 for the editing engine + Qwen3.**  TRAP: 4.45.2 does NOT recognize Qwen3; 5.12.1 supports Qwen3 but BREAKS the kmeng01/memit engine nethook (`IndexError` in compute_z). 4.51.0 = the window that supports both. Also tf 4.51 uses `torch_dtype=` (not 5.x `dtype=`).
- safetensors, numpy, accelerate (needed by tf for device_map).
- Editing engine: kmeng01/memit at `/workspace/memit_dry_run/memit` (UNMODIFIED).
- LARQL: Rust, `/workspace/external_prior_art/larql`. Build = `cargo build --release`. CLI binary `target/release/larql`.

## LARQL build deps (apt-installed — TRAPS for local)
1. **Rust** (rustup; minimal profile) — was absent.
2. **libssl-dev + pkg-config** — `larql-cli` links `openssl-sys` (model downloader).
3. **cmake + protobuf-compiler** — `protobuf-src` builds vendored protobuf via cmake.
4. **libopenblas-dev** — link error `-lopenblas` without it.
- Thread control: set `OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 RAYON_NUM_THREADS=8`. TRAP: default OpenBLAS spawns ~1 thread/core → on a many-core box, vindex `convert` THRASHES (system-time explodes, ~0 progress). Cap threads.
- I/O: run `convert`/serve off **local/tmpfs**, not the network FS, or it stalls.
- Backend: LARQL is **Metal-first** (`larql-compute-metal`); CPU path is what we used and it WORKS (positive control), but is less exercised by Chris.

## Models
- Qwen2.5-3B (`Qwen/Qwen2.5-3B` rev 3aab1f19…) — main editing study. hparams `qwen25_3b_memit_hparams.json` (band [4-8], v_loss 35, mom2_update_weight 5000, lm_head=embed_tokens tied).
- Qwen2.5-7B, GPT-J-6B — baselines.
- **Qwen3-0.6B** (`Qwen/Qwen3-0.6B`) — LARQL-servable deployment model. hparams `qwen3_06b_memit_hparams.json` (28 layers, band [4-8], v_loss 27). Qwen3 = qk-norm, NO attn bias (≠ Qwen2.5 which HAS bias — the LARQL-extraction bias bug only bites Qwen2/2.5).
- Gated models (Gemma) require HF license acceptance — NOT used (Qwen open).

## Durable vs ephemeral
- DURABLE (`/workspace/`): all `s2xx*.py` scripts, `*_hparams.json`, `covariance_caches/`, `build_vindex_overlay.py`, `CORPUS/`, `LARQL_INTEGRATION_ASSESSMENT.md`, `SESSION_CHECKPOINT.md`, `EVIDENCE_INDEX.md`, result `*.json`, `*.log`, `skills/`, `research_and_specs/`, `external_prior_art/`.
- EPHEMERAL (`/dev/shm/`): edited models, `.vlp` overlays, vindexes — RAM, lost on reboot, **reproducible from scripts**.
- Covariance compute cost: ~11–17 min/layer × 5 = ~70 min for a fresh model band (cached after).
