---
name: wide-intermediate-7b-editing-vram
description: "Running in-solve AlphaEdit on Qwen2.5-7B (intermediate 18944) on a 24GB 4090 needs eigh-not-svd for P, diagonal-add not L2*eye, del Pi before solve, expandable_segments, and BLAS=8 not 64"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f4d82a89-8dda-448d-8fc0-cf79fc2d6af9
---

In-solve AlphaEdit editing on **Qwen2.5-7B** (28 layers, intermediate **18944** → 18944² f32 = 1.4GB per P/cache/A matrix) on a 24GB RTX 4090 sits right at the VRAM wall (15.7GB model + several 1.4GB matrices). The working config for `experiments/track_b/b1_size_dose_response.py` (MODEL=7b):

1. **compute_P via `torch.linalg.eigh`, NOT `svd`.** cov (mom2 moment) is symmetric PSD → singular values == eigenvalues, so the null-space projector P (small-eigenvalue subspace, SAME threshold 0.005) is **mathematically identical**. `eigh` (cuSOLVER syevd) is fast + low-memory; cuSOLVER's dense `gesvd` **stalls for ~10+ min/layer** at n=18944 and needs ~Vh memory it doesn't have. (Verified: cov symmetry residual exactly 0.0.)
2. **`A = Pi@(Kg@Kg.T+ca); A.diagonal().add_(L2)`** — NOT `+ L2*torch.eye(n)`. The eye is a wasted 1.34GB allocation (the exact one that OOM'd); diagonal-add is **bit-identical** (proven `torch.equal`).
3. **`del Pi,Kg,rg; torch.cuda.empty_cache()` BEFORE `torch.linalg.solve(A,B)`** — Pi (1.4GB) isn't needed for the solve's LU workspace. Frees the last ~1.4GB.
4. **`torch.cuda.empty_cache()` after the inertness gate** (the gate leaves ~3GB residual that starves compute_P/edits).
5. Launch env: **`OMP/OPENBLAS/MKL_NUM_THREADS=8`** (NOT 64) + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. With SVD on GPU, high BLAS threads only **oversubscribe** the gate's CPU double-solves (load 44, slower); 8 is right. (64 was only ever needed for CPU SVD, which eigh-on-GPU eliminates.)

**compute_P SVD recomputes per PROCESS and is the iteration drag (2026-06-25, 3B).** Even with the covariance CACHED, `torch.linalg.svd(cov)` for the null-space projector P runs ~10-15 min/process on 3B (CPU SVD of 11008x11008 x5 layers) -- paid afresh on every small diagnostic run. Two fixes: (i) use **`eigh` not `svd`** here too (point 1 -- cov is symmetric PSD, mathematically identical, far faster); (ii) for iterative same-band runs, **cache P to disk** alongside the cov cache. This dominated wall-clock across the C1 diagnostic ladder (several short edit runs each gated behind a full re-SVD).

All of (1)-(4) are **value-preserving / proven inert** (LAW#5): in-place add, del, diagonal-add, eigh-for-symmetric — none change the computed ΔW. The inertness gate (memit mode) still passes |Δ|≈0. Process churn note: `pkill -f "MODEL=7b"` only kills the bash wrapper (env var not in python argv) → orphaned python keeps the GPU; kill the python PID directly. See [[runpod-durable-experiment-launch]], [[memit-cov-inversion-not-a-hang]].
