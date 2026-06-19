---
name: memit-cov-inversion-not-a-hang
description: "The \"frozen log + 0%|0/1000 + high CPU / GPU idle\" MEMIT pattern is normal cov-inversion compute, not a hang"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

When a MEMIT edit run on this pod shows a log frozen at `0%|...|0/1000` bars with 8+ CPU cores pinned and GPU at 0%, this is NOT a hang:

- The `0/1000` bars are `rome/layer_stats.py:155` cache-HIT loops running ZERO iterations (line 136 sets `ds=None` when the covariance npz already exists), so tqdm prints its initial `0/1000` and closes immediately.
- Covariance npz caches (e.g. `data/stats/EleutherAI_gpt-j-6B/wikipedia_stats/transformer.h.{3..8}.mlp.fc_out_float32_mom2_100000.npz`, ~1.07GB each) are present and reused — no recompute.
- The actual CPU burn (GPU idle) is the **covariance matrix inversion / CPU solve** (`_cov_cpu` P-VRAM-CPU-SOLVE) on ~16384-dim matrices — slow, no progress bar.

**To tell compute from deadlock:** measure /proc/<pid>/stat utime+stime delta over a few seconds. ~8 cores of jiffies = computing; ~0 = real deadlock. futex-waiting threads alone are just idle pool workers, not evidence of a hang.

Also: a buffered run hides the per-condition prints entirely — launch with `python -u` to see progress. See [[runpod-durable-experiment-launch]].
