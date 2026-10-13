## MOLAB MIGRATION ASSESSMENT (2026-06-17) — full report: `research_and_specs/molab_feasibility_report.md`
Verdict: **do NOT migrate the primary workflow.** Two decisive blockers (primary-sourced):
1. Storage — "limited" per-notebook R2 (object API, not POSIX; CF free R2 = 10GB) vs our 50–150GB tier; no documented path to seed 100GB (UI upload only). Partial fix: bring-your-own S3/R2 bucket via marimo `remote_storage` (fsspec/obstore) + a FUSE mount (rclone/s3fs); `mo.persistent_cache` for recomputables. Dissolves quota, not POSIX/seeding friction.
2. Unattended jobs — 90-min idle kills the CoreWeave sandbox; setsid/nohup survival undocumented (likely dies). marimo-pair runs Claude Code by writing CELLS into the remote sandbox from a LOCAL terminal — NOT a detached remote shell → our 3h detached-job pattern doesn't transfer.
GPU fine (RTX Pro 6000 sm_120 needs torch≥2.7.0+cu128) but determinism MUST be re-baselined (Ada→Blackwell fp16 differs).
- **molab niche:** bounded INTERACTIVE single-session (<12h) experiments where free 96GB GPU is the differentiator → the Gemma big-model probes the 4090 can't run (pull weights from own R2). NOT for long unattended sweeps.
- **Better unattended alternatives:** Modal (1TiB free persistent volumes, no session cap, subprocess OK, RTX Pro 6000 ~$3/h, ~$30/mo free credits) and Lightning AI (50–100GB POSIX persistent, full bash/SSH/tmux, ~80 free GPU-h/mo). RunPod (current) stays correct for production.
- **Before any pilot:** run report's UNKNOWN tests 1–2 (storage quota/POSIX) + 7–8 (background-job survival). Prompt that generated the report: `molab_viability_research_prompt.md`.

