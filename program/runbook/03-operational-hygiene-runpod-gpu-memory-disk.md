## §3 — OPERATIONAL HYGIENE (RunPod GPU / Memory / Disk)
═══════════════════════════════════════════════════════════════════════

### §3.1 — The dashboard-vs-pod trap (pod-era; note `runpod-dashboard-vs-pod-metrics` retired 2026-10-10, current disk policy §3.3a)
RunPod **dashboard** metrics diverge from in-pod tools — **trust the in-pod tools**:
- **GPU:** `nvidia-smi`. Dashboard util% lags and reflects OUR own work; the binding signal for "can my run allocate" is **`memory.used`** (we need ~6–16 GB depending on model). A run that loads and executes IS proof the GPU is ours.
- **RAM:** `free -h`. Dashboard % counts reclaimable page-cache; real pressure = `used`, not `used+cache`. We have ~450 GiB available.
- **Disk:** `df` inside the pod shows the **cluster** (1.2P), NOT our per-volume quota. The dashboard volume % (~86% now) is the binding, in-pod-invisible limit. **Respect it.**

### §3.2 — Pre-flight checklist (before every experiment)
1. `nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.free --format=csv,noheader` → confirm enough free VRAM; no foreign process holding memory.
2. Confirm needed cov caches exist (`covariance_caches/<model>/wikipedia_stats/*.npz`) — else queue cov compute first (§6).
3. Confirm `/dev/shm` headroom (`df -h /dev/shm`) for overlays/vindex; rebuild from scripts if wiped.
4. If a large download is pending, **reclaim disk first** (§3.3) — we're volume-constrained.
5. Launch detached + unbuffered (§2.8). Verify start (`ps`, `tail log`). Run the LAW#5 inertness gate.

### §3.3 — Disk reclamation (standing-auth — do it, narrate it)
Volume ~86% full. **~62 GB reclaimable** without touching the active Qwen line:
| Candidate | Size | Safe? |
|---|---|---|
| `hf_cache/hub/models--meta-llama--Llama-3.1-8B` | 15 GB | ✅ superseded baseline |
| `covariance_caches/meta-llama_Llama-3.1-8B` | 10 GB | ✅ |
| `covariance_caches/mistralai_Mistral-7B-v0.3` | 3.9 GB | ✅ |
| `covariance_caches/meta-llama_Llama-3.2-3B` | 1.8 GB | ✅ HALTED experiment |
| `stage_1_sect/overlays` | 33 GB | ⚠️ confirm not referenced before delete |
Reclaim the first four (~31 GB) freely; verify `stage_1_sect/overlays` provenance before removing. Always keep: Qwen2.5-3B/7B, Qwen3-0.6B, their cov caches, the engine, LARQL, CORPUS, memory_mirror.

### §3.3a — Storage & archival policy (operator, 2026-10-09; BINDING after the 110 GB disk-full incident)
Incident: the C10Y pre-cast diagnostic wrote 105 GB of float64 operand packets, filled `/Volumes/memit`, and killed ASTRA attempt 4's first start (infra; relaunched under Astra RELAUNCH-OK). Operator: offloading 105 GB onto the internal SSD "isn't acceptable"; "we need much better solutions for managing disc space and file archival".
- **Classify every artifact at write time.** *Science records* (JSON, manifests, hashes, summaries, CORPUS, ledgers, code) → git (durable tier). *Regenerable bulk* (operand/tensor packets, harvest tensors, caches reproducible from pinned code + inputs) → hot tier (memit) only while an analysis needs it.
- **Retention:** once a run's reading is confirmed (Astra CONFIRM / close-out), or it is INCONCLUSIVE with no claim drawn, record per-file SHA-256 + sizes in git, keep at most a minimal sample a named follow-up needs, delete the rest. Deleting regenerable bulk under this rule removes no science: claims rest on records, hashes and frozen code/inputs.
- **Irreplaceable bulk** (non-regenerable, too big for git) → remote archive **Google Drive via rclone** (operator choice 2026-10-09; rclone v1.75.2 installed; remote `gdrive:` **AUTHORIZED 2026-10-10** — scope drive.file, Gmail Drive 5 TiB, OAuth app published so the token does not expire; setup + traps: `memory_mirror/gdrive-rclone-remote.md`). Never the internal SSD.
- **Every scope/prereg states a disk budget** (bytes per packet × count) beside time and memory; every queue/launcher waits for free disk ≥ projected writes + 20 GiB before dispatch.
- **Approved:** replace the 6-hourly internal-SSD mirror of memit (`tools/backup_mirror.sh`, ~266 GB at `~/Backups/memit`) with a Drive backup once `gdrive` is authorized.
- **Drive backup build (2026-10-10):** host self-tests PASS on real Drive; upload 1.16 MB/s, first full copy ≈ 69 h, day-capped by operator choice (D-C10r-rulings-15); Astra r1 NO-GO → fixes in build; activation waits for the PR #21 merge + a never-dialog applet with the operator's one-time Removable Volumes grant. Detail: [backup build report](results/backup_gdrive_build_report.md), [host findings](results/backup_gdrive_host_20261010/HOST_FINDINGS.md). **2026-10-11:** the backup-only release merged as PR #22 → master 5ccbb836 (D-C10r-gitmerge-2); activation awaits the operator's three OKs (full read-back, write pause, fresh history vs recovery).
- First application: pre-cast operands hashed (`results/c10y_precast_diag/20261009T225619Z/OPERANDS_SHA256SUMS.txt`, 131 files), A7-L4 set kept on memit for the controls-timing measurement, the other 96 (86 GB) approved for deletion from `~/Backups/memit_offload/`.

### §3.4 — Cov-cache & /dev/shm discipline
- Covariance is the expensive precompute (~1–2 h per 5-layer band on a 3B). It **caches to `covariance_caches/<model>/wikipedia_stats/`** — reuse aggressively; never recompute a cached band.
- `/dev/shm` (29 GB RAM tmpfs) holds vindex/overlays for speed; it is **ephemeral** — rebuild from scripts after a pod restart. Cap BLAS threads (`OPENBLAS_NUM_THREADS=8`) so cov inversion doesn't thrash.
- transformers pinned **4.51.0**; torch 2.4.1+cu124. Do not upgrade in place (breaks engine nethook / Qwen3 support balance).

═══════════════════════════════════════════════════════════════════════
