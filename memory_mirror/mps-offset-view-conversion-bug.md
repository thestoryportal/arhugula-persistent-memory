---
name: mps-offset-view-conversion-bug
description: torch 2.8 MPS silently corrupts t.to(device="cpu", dtype=X) when t is an offset view and X != t.dtype — use .cpu().to(X); clone-first is not reliable
metadata:
  type: project
---
Verified 2026-10-08 (torch 2.8.0, Apple MPS): for an MPS tensor with `storage_offset() != 0`, `t.to(device="cpu", dtype=X)` with `X != t.dtype` returns WRONG data with no error — all zeros for a random fp16 row, ~1e8 garbage in the ASTRA driver. Holds fp16→fp32 and fp32→fp16, any offset. `contiguous()` does not help (already contiguous, offset kept). Correct ONLY: `t.cpu().to(X)` or `t.to(X).cpu()` (0 failures in the audit). `clone()` first is NOT safe (1/50 wrong when narrowing). Same-dtype `.to("cpu")` is fine; CPU→MPS and MPS→MPS conversions tested fine (incl. weight writes `upd.to(w.device, w.dtype)`); float64 targets raise on MPS (loud). Wider than the `.to` form: any MPS→CPU copy that also changes dtype is affected — `cpu_buf.copy_(v)`, assignment into a CPU tensor of another dtype, `torch.as_tensor/torch.tensor(v, device='cpu', dtype=X)`, `.to(cpu_tensor)`, `.type(torch.FloatTensor)`. Narrowing/same-width MPS→CPU casts (fp32→fp16/bf16, fp16↔bf16, int64→int32) can also overwrite the MPS SOURCE tensor, intermittently, even at offset 0.

It caused ASTRA attempt 2 HALTED-V5 (Z0 "spread" 1.13e8): `margin_leads` (c10z_astra_arms.py:224) converts `model(...).logits[0,-1]` this way; the batch path gathers into fresh offset-0 tensors and was correct. The Z0 instrument gate caught it — a gate working as designed.

**Why:** any typical indexing (`x[0,-1]`, `x[:, i]`, `select`, `narrow`, `split`) yields offset views, so the corruption is silent and can enter any recorded number.

**How to apply:** never combine device and dtype in one MPS→CPU step; always `.cpu()` first, then `.to(dtype)`. No CORPUS 41–57 result was affected (audit 2026-10-08); only ASTRA (no CORPUS entry) and the z0 probes (native/full fields invalid). Every build brief requires an AST test forbidding the combined form. Audit: results/mps_offset_conversion_audit.md. Related: [[fp32-reductions-over-big-tensors]], [[seed-freezes-context-templates]].
