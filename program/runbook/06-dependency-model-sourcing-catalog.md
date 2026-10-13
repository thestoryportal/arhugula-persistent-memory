## §6 — DEPENDENCY & MODEL SOURCING CATALOG
═══════════════════════════════════════════════════════════════════════

### §6.1 — Already cached (no download)
| Asset | Size | Location | Ready for |
|---|---|---|---|
| Qwen2.5-3B + cov [4-8] | 5.8 GB + cov | hf_cache + covariance_caches | A1, A2, A3, all Track A |
| Qwen2.5-3B cov [18-22] (mid-late) | computing now (~done) | covariance_caches | A4 band test |
| Qwen2.5-7B + cov | 15 GB + 6.7 GB | cached | clean-reference checks |
| Qwen3-0.6B + cov [4-8] | 1.5 GB | cached | bridge/serve, Track E |
| AlphaEdit/WISE/GRACE/MEMIT refs | — | `easyedit_upstream/easyeditor/models/*`, `easyedit_assets/rung*` | A3/A5/A6 ports |
| LARQL binary | 119 MB | `code/vendor/external_prior_art/larql/target/release/larql` | bridge, B3, E |

### §6.2 — To source downstream (reclaim disk first — §3.3)
| Asset | Source | Size | Download | Cov-compute | Needed by |
|---|---|---|---|---|---|
| **Qwen3-4B** | HF `Qwen/Qwen3-4B` | ~8 GB | ~15–30 min | ~1.5–2.5 h (5-layer band) | **B1** (scale + BetaEdit anchor) |
| **Qwen3-1.7B** | HF `Qwen/Qwen3-1.7B` | ~3.4 GB | ~5–15 min | ~1–2 h | A6 (SAE), B1-small |
| **Qwen3-8B** | HF `Qwen/Qwen3-8B` | ~16.4 GB | ~30–60 min | ~2–4 h | A6 (SAE), B1-large |
| **Qwen-Scope SAEs** | HF `Qwen/SAE-Res-Qwen3-{1.7B,8B}-*` | ~hundreds MB–GB each (verify at pull) | minutes–tens | n/a | A6 frontier |
| **llama.cpp prebuilt** | `github.com/ggml-org/llama.cpp/releases` `b9693 ubuntu-x64` | ~tens MB | minutes | n/a | B3 real Q4_K |
| **BetaEdit** | OFFICIAL repo lbq8942/BetaEdit (IJCAI 2026); cloned to code/vendor/external_prior_art/BetaEdit; ships qwen2.5-3b config = our exact band[4-8]/down_proj/subject_last setup | — | PORT the solve into our harness (~hours, builds on `g6_scale_n.py`/`a2_relbal_sentinels.py`) | reuse cached cov | A3 |
| **DiKE** (optional) | arXiv 2505.18774 | — | reimplement disentanglement module | — | A6-adjacent |

═══════════════════════════════════════════════════════════════════════
