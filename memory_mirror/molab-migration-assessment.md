---
name: molab-migration-assessment
description: Whether to move the GPU work from RunPod to molab (marimo) free tier — verdict and why
metadata: 
  node_type: memory
  type: project
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

Assessed 2026-06-17 (full report: `research_and_specs/molab_feasibility_report.md`; research prompt: `/workspace/molab_viability_research_prompt.md`).

**Verdict: do NOT migrate the primary MEMIT-editing workflow to molab free tier.** Two decisive, primary-sourced blockers:
1. **Storage** — "limited" per-notebook Cloudflare-R2 (object API, NOT POSIX; CF's free R2 = 10 GB) vs our 50–150 GB working tier (model weights + cov caches). No documented way to seed ~100 GB (UI upload only). Partial fix: bring-your-own S3/R2 bucket via marimo `remote_storage` (fsspec/obstore) + FUSE mount (rclone/s3fs); `mo.persistent_cache` for recomputable artifacts. Dissolves the quota, not the POSIX/seeding friction.
2. **Unattended jobs** — 90-min idle shutdown kills the CoreWeave sandbox; setsid/nohup survival undocumented (likely dies). marimo-pair runs Claude Code by writing CELLS into the remote sandbox from a LOCAL terminal — not a detached remote shell. Our 3h `setsid` detached-job pattern does not transfer.

GPU is fine (RTX Pro 6000 96GB, sm_120 — needs torch≥2.7.0+cu128) BUT determinism must be re-baselined (Ada→Blackwell fp16 reduction order differs; not bit-exact across architectures).

**Right uses:**
- molab niche = bounded INTERACTIVE single-session (<12h) experiments where the free 96GB GPU is the differentiator → the Gemma big-model probes the 4090 can't run (see [[gemma4-rung4-candidate]]), pulling weights from own R2.
- For cheaper UNATTENDED GPU + persistent storage: **Modal** (1TiB free volumes, no session cap, subprocess OK, RTX Pro 6000 ~$3/h, ~$30/mo credits) or **Lightning AI** (POSIX persistent, full bash/tmux, ~80 free GPU-h/mo) fit our workflow far better.
- RunPod (current) remains correct for the production program.

Before any pilot: run report UNKNOWN tests 1–2 (storage quota/POSIX) + 7–8 (background-job survival past idle). Relates to [[runpod-durable-experiment-launch]] (the detached-job pattern molab lacks).
