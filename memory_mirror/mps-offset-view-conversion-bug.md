---
name: mps-offset-view-conversion-bug
description: torch 2.8 MPS silently corrupts t.to(device="cpu", dtype=X) when t is an offset view and X != t.dtype — use .cpu().to(X) or clone() first
metadata:
  type: project
---
Verified 2026-10-08 (torch 2.8.0, Apple MPS): for an MPS tensor with `storage_offset() != 0`, `t.to(device="cpu", dtype=X)` with `X != t.dtype` returns WRONG data with no error — all zeros for a random fp16 row, ~1e8 garbage in the ASTRA driver. Holds fp16→fp32 and fp32→fp16, any offset. `contiguous()` does not help (already contiguous, offset kept). Correct: `t.cpu().to(X)`, `t.to(X).cpu()`, `t.clone().to(...)`; same-dtype `.to("cpu")` and offset-0 tensors are fine; float64 targets raise on MPS (loud).

It caused ASTRA attempt 2 HALTED-V5 (Z0 "spread" 1.13e8): `margin_leads` (c10z_astra_arms.py:224) converts `model(...).logits[0,-1]` this way; the batch path gathers into fresh offset-0 tensors and was correct. The Z0 instrument gate caught it — a gate working as designed.

**Why:** any typical indexing (`x[0,-1]`, `x[:, i]`, `select`, `narrow`, `split`) yields offset views, so the corruption is silent and can enter any recorded number.

**How to apply:** never write a combined device+dtype conversion on a tensor that may be MPS; write `.cpu().to(dtype)`. Every build brief requires an AST test forbidding the combined form. Audit: results/mps_offset_conversion_audit.md. Related: [[fp32-reductions-over-big-tensors]], [[seed-freezes-context-templates]].
