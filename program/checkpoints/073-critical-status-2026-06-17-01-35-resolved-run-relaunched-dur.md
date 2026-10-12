## CRITICAL STATUS (2026-06-17 01:35) — RESOLVED, run relaunched durably
- **The original GPT-J GATE-CAL run (PID 44350, started 01:01 by a since-disconnected session) DIED at ~01:28 with NO output** — killed by the disconnect (its whole process group, python+bash wrapper, vanished together; GPU freed). NOT a crash: no traceback.
- **Diagnosis of the "frozen log / 0%|0/1000 / high-CPU-GPU-idle" pattern (do not be misled by it again):**
  - The `0%|...|0/1000` bars are MEMIT `rome/layer_stats.py:155` cache-HIT loops running ZERO iterations (line 136: `ds=None` when the cov npz exists). They print their initial `0/1000` and close instantly — they are NOT a hang.
  - Covariance npz caches for layers 3–8 are present & valid (6×1.07GB, Apr 26) — NOT being recomputed.
  - The real CPU burn (8+ cores, GPU idle) is the **covariance matrix inversion / CPU solve** (`_cov_cpu` P-VRAM-CPU-SOLVE) on ~16384-dim matrices — legitimately slow, no progress bar. Verified compute (not deadlock): 8.2 cores busy via /proc jiffies delta; futex-waiting threads are just idle pool workers.
  - The frozen log was Python **block-buffered stdout** hiding the per-condition prints — NOT a stall.
- **Action taken:** relaunched UNBUFFERED + DETACHED so progress is visible and disconnect-proof.
  - Command: `setsid bash -c 'cd /workspace && PYTHONUNBUFFERED=1 MODEL=gptj python -u s241_gatecal.py > s241_gatecal_gptj.log 2>&1' </dev/null & disown`
  - Current PID **49432**, own session SID 49431 (separate from claude's session → SIGHUP on disconnect cannot reach it).
  - Old buffered dead-run log preserved at `s241_gatecal_gptj.deadrun_0103.log`.

