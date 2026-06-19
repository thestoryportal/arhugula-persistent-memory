---
name: runpod-dashboard-vs-pod-metrics
description: "RunPod dashboard GPU/RAM/disk % diverge from in-pod tools; nvidia-smi memory.used is the binding GPU signal, util% just reflects/lags our own work"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e1b2ae2b-4a31-42c8-a24d-462bcf751e0d
---

The RunPod **dashboard** metrics (GPU util %, system memory %, network volume %) repeatedly diverged from the **authoritative in-pod tools** this session (2026-06-18) — cost attention three times (RAM, disk, GPU). Trust the in-pod tools:

- **GPU:** dashboard showed "100% utilization" while `nvidia-smi` showed 0% util / 2 MiB used / 24 GB free. The dashboard util% **lags and reflects our OWN recent/current work** (MEMIT `compute_z` saturates cores in bursts). The binding signal for "can my run allocate" is **`nvidia-smi` memory.used**, NOT util%. A run loading 7.6 GB and executing IS the proof the GPU is ours — high util% during a run is healthy, not contention.
- **RAM:** dashboard "74-86%" = `(used + buff/cache)/total`. `free -h` showed only ~33 GiB truly used, ~450 GiB available — the rest is reclaimable page cache (cov caches/models). Not real pressure.
- **Disk/volume:** `df` inside the pod shows the underlying RunPod **MFS cluster** (1.2P, ~65%), NOT the per-volume quota. The operator/dashboard volume % IS the binding, in-pod-invisible constraint — respect it; minimize new `/workspace` writes; write transient artifacts (test vindexes) to `/dev/shm` or delete after use; reuse cached covariance. **RECURRED 2026-06-18 (E1):** I read `df`=65% and declared "disk not a constraint" — operator corrected to **93% volume used**. Don't re-trust `df` for the volume; treat the operator's number as ground truth. Biggest reclaimable category turned out to be **stale non-Qwen models in `hf_cache/hub`** (Mistral-7B 28 G, Llama-3.1-8B 15 G + a duplicate 15 G, GPT-J 12 G, Llama-3.2-3B 6 G, concluded-stale chrishayuk gemma-3-4b vindexes ~17 G ≈ **91 G**) — all re-pullable from HF Hub; then **orphaned cov caches** whose models you just deleted (cov is useless without its model: Llama-8B 10 G, Mistral 3.9 G, Llama-3.2-3B 1.8 G) + stale `stage_1_sect/overlays` (33 G). Freed 136 G total (248→112 G, ~93%→~42%) keeping only Qwen2.5-3B/Qwen3-0.6B + Qwen2.5-3B cov + B3 artifacts + engine/larql. Operator kept Qwen2.5-7B (+cov) and wikipedia for B1/future-cov.

Rule: before worrying about a dashboard number, check the in-pod tool (`nvidia-smi` / `free -h` / `df`) — EXCEPT for the **volume quota**, where `df` is misleading (cluster pool) and the operator/dashboard % is binding. For GPU-availability decisions, run a small smoke test — if it loads + executes, the GPU is available regardless of the dashboard. See [[runpod-durable-experiment-launch]].
