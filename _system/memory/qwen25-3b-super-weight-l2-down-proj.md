---
name: qwen25-3b-super-weight-l2-down-proj
description: Qwen2.5-3B super weight at L2 down_proj[318,3189]; the band's norm-98 first-token key is its super activation; keep it high-precision in GGUF.
metadata:
  type: project
---

# Qwen2.5-3B has a super weight at layer 2 `down_proj[318, 3189]`; the band's first-token key (norm 98 at L4) is its super activation

**Fact (2026-10-04; `results/superweight_qwen3b.json`, `results/superweight_qwen3b_prune_check.json`; scripts `experiments/track_c/superweight_locate_qwen3b.py`, `superweight_prune_check_qwen3b.py`; method Yu et al. 2024, arXiv 2411.07191, `docs/PRIOR_ART_SWEEP_2026-10-04.md` §7):** one data-free forward pass finds a single candidate by the paper's rule — layer 2, `mlp.down_proj[318, 3189] = −0.5508` (input spike 4860, output spike 2820, both at token 0). Zeroing that one scalar in memory raises mean NLL 1.962 → 2.755 nats (perplexity 7.11 → 15.72 on four sentences); restoring it returns the model exactly. Residual channel 318 carries the first-token super activation through L1–L4, L16–L17, L30, L33, L35. At L4 the `down_proj` input spike is 98 at token 0 — the same "attention-sink first-token key, norm 98 in all 24 sequences" that Route A F4 (`docs/C10K_ROUTEA_RESULT.md`) found dominating the L4 preservation term.

**How to apply:** the MEMIT band [4–8] does not touch layer 2, so edits never rewrite the super weight; but every band key set contains the super activation at token 0, which the Wikipedia covariance over-protects — name it as such rather than as an anomaly. Before trusting any Q4_K_M survival number, check that the exported GGUF keeps `layers.2.mlp.down_proj[318, 3189]` and the channel-318 activation at high precision (the paper's keep-super-weight / clip-others recipe). Any model swap: re-run the locate script first (one forward pass).
