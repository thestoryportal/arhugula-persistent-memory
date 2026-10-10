---
name: fp32-reductions-over-big-tensors
description: A cosine/dot over a flattened full-size delta (22.5M fp32 elements) drifts ~0.8% and can exceed 1; compute in float64
metadata:
  type: feedback
---
2026-10-08: C10W P2 eval HALTED at its very last validity check because `c10w_oracle_eval.py:434–440` computed the same-seed ΔW cosine with an fp32 `torch.dot` over the flattened 2048×11008 merged delta: 1.007–1.009 (> 1), while float64 gives 1.0000000000 and the retrain was bit-identical. ~103 GPU-min of scoring finished but no reading was issued.

**Why:** fp32 accumulation over tens of millions of terms loses ~1%; `norm()` and `dot()` lose differently, so ratios leave their mathematical range. A diagnostic placed after the scoring can void a whole stage.

**How to apply:** in any driver/reader, do reductions over model-sized tensors (dot, cosine, Frobenius ratios) in float64; in pre-run reviews, check that validators with range bounds (|cos| ≤ 1) cannot trip on precision; run cheap diagnostics before the expensive scoring when possible. Related: [[gpu-gate-blocks-any-python]].
