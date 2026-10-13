# molab Feasibility Report: MEMIT-Class LLM Weight-Editing Workload

**Generated:** June 17, 2026  
**Workload:** In-weight, MEMIT-class knowledge editing of LLMs in PyTorch + HuggingFace Transformers (fp16)  
**Current host:** Paid RunPod RTX 4090 (24 GB)  
**Candidate:** molab free tier (RTX Pro 6000 Blackwell 96 GB, 4 CPU, 32 GB RAM, 12h sessions, 90-min idle shutdown)

---

## Workload Characteristics

- Models: GPT-J-6B, Qwen2.5-7B, Llama-3.2-3B, possibly Gemma 4 12B–31B
- Per-layer covariance statistics: ~1 GB .npz each, several per model
- Persistent working tier: 50–150 GB (model weights 10–30 GB + covariance caches + artifacts)
- Job duration: 30 min to 3+ hours; currently run as detached setsid/nohup processes
- Automation: Claude Code CLI agent driving work from a terminal
- Reproducibility gates: bit-exact cross-session determinism, known-baseline reproduction

---

## Section 1 — Persistent Storage (DECISIVE)

### What is documented

- molab provides **"a limited amount of persistent storage per notebook."**  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH** (official)  
  **Exact quota is NOT stated anywhere in official documentation. This is a decisive unknown.**

- Storage backend is **Cloudflare R2**, described as a "zero-egress object store."  
  Source: [marimo.io/blog/announcing-molab](https://marimo.io/blog/announcing-molab) | Strength: **HIGH**

- Access from inside a notebook session is via a **file tree sidebar panel** for UI file uploads.  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH**

- The download button **"brings just the notebook file down, and does not include your attached storage."**  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH**

- Storage persists across sessions (implied by R2 backing), but **no explicit retention/expiry policy is documented.**  
  Strength: **MEDIUM** (inference from R2 architecture)

### Cloudflare R2 object storage characteristics

- R2 is **S3-compatible object storage, NOT a POSIX filesystem.** Access is via object API (GET/PUT/DELETE), not `open()` / `mmap()` / `os.listdir()`.  
  Source: [developers.cloudflare.com/r2/pricing](https://developers.cloudflare.com/r2/pricing/) | Strength: **HIGH**

- Object size limit: **5 TiB per object** (single-part upload max: ~5 GiB; multipart: ~4.995 TiB).  
  Source: [developers.cloudflare.com/r2/platform/limits](https://developers.cloudflare.com/r2/platform/limits/) | Strength: **HIGH**

- Cloudflare's own public free tier for R2: 10 GB/month storage + 1M Class A + 10M Class B ops. Whether molab's allocation mirrors this or is larger is **UNKNOWN.**  
  Source: [developers.cloudflare.com/r2/pricing](https://developers.cloudflare.com/r2/pricing/) | Strength: **HIGH** (for CF free tier); **UNKNOWN** for molab's allocation

- Read/write latency: object-store HTTP latency (tens–hundreds of ms per request for metadata); sequential throughput at scale can reach several hundred MB/s but is not SLAed for notebook workloads.  
  Strength: **MEDIUM** (general CF network performance; no molab-specific benchmark)

### Critical gaps for this workload

- The 50–150 GB working tier almost certainly **exceeds molab's free per-notebook quota**, but the quota is undocumented.
- Even if quota were sufficient, R2 is an **object store, not a mounted POSIX filesystem.** Whether molab presents it as a POSIX path (via FUSE or similar) or exposes it only as an object API is **UNKNOWN** — and decisive, since all existing code uses standard file paths (`np.save()`, HuggingFace `~/.cache`, etc.).

---

## Section 2 — Terminal & Background Processes

### What is documented

- molab officially supports **agent CLIs** including **Claude Code, Codex, and OpenCode** via the "marimo pair" feature.  
  Source: [docs.marimo.io/guides/generate_with_ai/marimo_pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/) | Strength: **HIGH**

- The mechanism: start a notebook on molab → click "Pair with an agent" in the actions panel → follow instructions to connect a **local** Claude Code terminal to the **remote** molab sandbox. Code is written as notebook cells.  
  Source: [docs.marimo.io/guides/generate_with_ai/marimo_pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/) | Strength: **HIGH**

- **"Use your agent from the terminal as normal, but all the Python code would be written into the notebook in the molab sandbox."**  
  Source: [docs.marimo.io/guides/generate_with_ai/marimo_pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/) | Strength: **HIGH**  
  Implication: agent actions materialize as **notebook cells**, not as an independent shell process.

- molab runs on **CoreWeave sandboxes.**  
  Source: [marimo.io/blog/reintroducing-molab](https://marimo.io/blog/reintroducing-molab) | Strength: **HIGH**

### What is NOT documented

- Whether molab provides a raw shell/terminal separate from the notebook UI. **UNKNOWN.**
- Whether `nohup`, `setsid`, `tmux`, or `screen` can be run inside a molab session to create jobs that outlive browser connection. **UNKNOWN.**
- Whether CoreWeave's sandbox kills all child processes on session/idle timeout. **UNKNOWN** (official); likely yes based on standard cloud sandbox behavior. Strength: **MEDIUM** (inference)
- The 90-minute idle shutdown almost certainly applies to the **entire compute environment**, meaning any background `nohup` processes would also be killed. Strength: **MEDIUM** (inference; not explicitly documented)

### Key concern

The marimo pair / Claude Code integration routes all code through notebook cells, not through a detached shell. The current workflow of `setsid python train.py &` → disconnect terminal → job runs 3+ hours is **fundamentally incompatible with the documented architecture** unless a separate shell is available (undocumented).

---

## Section 3 — GPU Specifics

### Confirmed hardware specs

| Parameter | Value | Source | Strength |
|---|---|---|---|
| GPU model | NVIDIA RTX PRO 6000 Blackwell Workstation Edition | [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | HIGH |
| VRAM | 96 GB GDDR7 with ECC | [NVIDIA spec sheet PDF](https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/rtx-pro-6000-blackwell-workstation-edition/workstation-blackwell-rtx-pro-6000-workstation-edition-nvidia-us-3519208-web.pdf) | HIGH |
| Memory bandwidth | 1,792 GB/s | [NVIDIA spec sheet PDF](https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/rtx-pro-6000-blackwell-workstation-edition/workstation-blackwell-rtx-pro-6000-workstation-edition-nvidia-us-3519208-web.pdf) | HIGH |
| CUDA cores | 24,064 | [bizon-tech.com RTX Pro 6000 specs](https://bizon-tech.com/blog/new-rtx-pro-6000-blackwell-gpus-tech-specs) | HIGH |
| Tensor cores | 752 | [bizon-tech.com RTX Pro 6000 specs](https://bizon-tech.com/blog/new-rtx-pro-6000-blackwell-gpus-tech-specs) | HIGH |
| Compute capability | **sm_120 / CC 12.0** | [developer.nvidia.com/cuda/gpus](https://developer.nvidia.com/cuda/gpus) + [pytorch/pytorch#157549](https://github.com/pytorch/pytorch/issues/157549) | HIGH |
| Minimum driver | R570+ | [NVIDIA CUDA migration guide](https://forums.developer.nvidia.com/t/software-migration-guide-for-nvidia-blackwell-rtx-gpus-a-guide-to-cuda-12-8-pytorch-tensorrt-and-llama-cpp/321330) | HIGH |
| Required CUDA | 12.8+ for native sm_120 | [NVIDIA CUDA migration guide](https://forums.developer.nvidia.com/t/software-migration-guide-for-nvidia-blackwell-rtx-gpus-a-guide-to-cuda-12-8-pytorch-tensorrt-and-llama-cpp/321330) | HIGH |

### PyTorch sm_120 status (DECISIVE)

- sm_120 support was **added in PyTorch 2.7.0+cu128** (stable release). Earlier wheels (2.5.x, 2.6.x, or 2.7.x+cu124) will fail with "no kernel image available for execution on the device."  
  Source: [discuss.pytorch.org sm_120 thread](https://discuss.pytorch.org/t/pytorch-support-for-sm-120-nvidia-geforce-rtx-5060/220941) | Strength: **HIGH**

- Live test on RTX Pro 6000 Blackwell with `torch 2.7.1+cu128` confirms: `['sm_75', 'sm_80', 'sm_86', 'sm_90', 'sm_100', 'sm_120', 'compute_120']`  
  Source: [pytorch/pytorch#157549](https://github.com/pytorch/pytorch/issues/157549) | Strength: **HIGH** (primary source live test)

- molab docs state "torch" is pre-installed but do **NOT** specify the version.  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH** (source is explicit about incompleteness)  
  Whether the pre-installed torch is ≥2.7.0+cu128: **UNKNOWN without testing.**

- CUDA/driver version in molab environment: **NOT stated in any official documentation. UNKNOWN.**

### GPU-time quota / fair use

- No GPU-hours/month limit, no credit system, and no fair-use throttling threshold is published. Only policy: **"free, as long as usage is reasonable."**  
  Source: [marimo.io/blog/reintroducing-molab](https://marimo.io/blog/reintroducing-molab) | Strength: **HIGH** (source), critically vague
- GPU availability / queueing wait time on free tier: **UNKNOWN.**

---

## Section 4 — Environment Control

### What is documented

- Pre-installed packages include `torch`, `numpy`, `polars`, and "more."  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH**

- Package installation uses **uv** (via marimo's built-in package manager sidebar); described as "lighting-fast." Specific version pinning is supported via the sidebar panel.  
  Source: [marimo.io/blog/announcing-molab](https://marimo.io/blog/announcing-molab) | Strength: **HIGH**

- Reproducible and configurable environment management is listed as a **planned future feature**, not currently available.  
  Source: [marimo.io/blog/reintroducing-molab](https://marimo.io/blog/reintroducing-molab) | Strength: **HIGH**

### What is NOT documented

| Item | Status |
|---|---|
| OS version / kernel | UNKNOWN |
| root / sudo access | UNKNOWN |
| `apt-get` availability | UNKNOWN |
| `pip install` directly (vs uv only) | UNKNOWN |
| Internet egress (general) | UNKNOWN (GitHub notebook access implies outbound HTTP; not explicitly stated) |
| HuggingFace gated model downloads with `HF_TOKEN` | UNKNOWN |
| HF cache location (persistent vs ephemeral) | UNKNOWN — if `~/.cache/huggingface/` is on ephemeral local disk, it is wiped every session |
| `git clone` access | UNKNOWN |

---

## Section 5 — Free-Tier Limits / "Reasonable Use"

### Documented limits

| Parameter | Value | Source | Strength |
|---|---|---|---|
| Session length | **12 hours max** | [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | HIGH |
| Idle shutdown | **90 minutes inactivity** | [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | HIGH |
| Default CPU | 4 vCPUs | [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | HIGH |
| Default RAM | 32 GB | [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | HIGH |
| GPU VRAM | 96 GB (RTX Pro 6000) | [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | HIGH |
| Cost | Free, "reasonable use" | [marimo.io/blog/reintroducing-molab](https://marimo.io/blog/reintroducing-molab) | HIGH |
| GPU-hours/month | **NOT DOCUMENTED** | — | — |
| Concurrent notebooks | **NOT DOCUMENTED** | — | — |
| Bandwidth cap | **NOT DOCUMENTED** | — | — |
| "Reasonable use" definition | **NOT DOCUMENTED** | — | — |

### Risk assessment

- Running 12-hour GPU sessions daily on a 96 GB card for a multi-week research project is non-trivially at risk of informal throttling or account action under an undefined "reasonable use" policy.  
  Strength: **MEDIUM** (inference from standard freemium practice; not stated explicitly)

- molab is in **"public preview"**; pricing and access terms may change.  
  Source: [marimo.io/blog/reintroducing-molab](https://marimo.io/blog/reintroducing-molab) | Strength: **HIGH**

---

## Section 6 — Determinism Across Hardware (Blackwell CC 12.0 vs Ada CC 8.9)

### PyTorch official position

- **"Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different platforms."**  
  Source: [pytorch.org/docs/stable/notes/randomness](https://pytorch.org/docs/stable/notes/randomness.html) | Strength: **HIGH**

- **"Results may not be reproducible between CPU and GPU executions, even when using identical seeds."**  
  Source: [pytorch.org/docs/stable/notes/randomness](https://pytorch.org/docs/stable/notes/randomness.html) | Strength: **HIGH**

- Within-run determinism is achievable with:  
  `torch.use_deterministic_algorithms(True)` + `CUBLAS_WORKSPACE_CONFIG=:4096:8` + `torch.backends.cudnn.deterministic=True` + fixed seeds.  
  Source: [pytorch.org/docs/stable/notes/randomness](https://pytorch.org/docs/stable/notes/randomness.html) | Strength: **HIGH**

### Cross-architecture (Ada CC 8.9 → Blackwell CC 12.0)

- **NVIDIA does not guarantee numerical/bit-exact cross-architecture results.** Blackwell introduces a new compute capability major version (12) vs Ada Lovelace (8.9). Different SM shared memory configuration (128 KB/SM on CC 12.0), different warp concurrency (48 vs 64 concurrent warps/SM on CC 10.0), and different scheduler behavior means fp16 matmul reduction order can differ.  
  Source: [docs.nvidia.com/cuda/blackwell-tuning-guide](https://docs.nvidia.com/cuda/blackwell-tuning-guide/index.html) | Strength: **HIGH**

- For fp16 transformer forward passes, cuBLAS selects tiling strategies based on SM count and architecture. An RTX 4090 (Ada, 16,384 CUDA cores, CC 8.9) and an RTX Pro 6000 Blackwell (24,064 CUDA cores, CC 12.0) will use **different cuBLAS kernels**, producing different floating-point reduction orders and therefore **different numerical results for fp16 matmul.**  
  Strength: **HIGH** (CUDA determinism docs + IEEE 754 non-associativity of fp16 addition)

- Community confirmation: PyTorch forum explicitly confirms different GPU types produce different results even with full determinism flags. **"I don't think this is universally possible due to the different hardware architectures."**  
  Source: [discuss.pytorch.org/t/different-result-on-different-gpu/102502](https://discuss.pytorch.org/t/different-result-on-different-gpu/102502) | Strength: **MEDIUM** (community, consistent with primary source)

- Independent Thread Scheduling differences between architectures can alter which threads participate in warp-level operations.  
  Source: [docs.nvidia.com/cuda/blackwell-compatibility-guide](https://docs.nvidia.com/cuda/blackwell-compatibility-guide/) | Strength: **HIGH**

### Conclusion on determinism

**You must re-baseline all determinism gates when migrating from RTX 4090 (Ada, CC 8.9) to RTX Pro 6000 Blackwell (CC 12.0).** Bit-exact cross-architecture results are not achievable with standard PyTorch. Within-session reproducibility on Blackwell is achievable with the full determinism flag suite above.

---

## Section 7 — Marimo as Framework

### Reactive model implications

- marimo **re-runs a cell's descendants** when any of its defined global variables change. Re-runs are triggered by variable definitions changing, not by time or user input mid-execution.  
  Source: [docs.marimo.io/guides/reactivity](https://docs.marimo.io/guides/reactivity/) | Strength: **HIGH**

- A cell running a 3-hour training loop will **NOT be interrupted mid-run** by reactive re-execution. However, if a variable from that cell is depended upon by a downstream cell, and something upstream changes, marimo will queue a re-run of the cell **after** it finishes.  
  Strength: **HIGH** (follows from DAG semantics)

- marimo uses a **lazy runtime option**: mark cells as stale instead of auto-running, to prevent cascading re-runs in expensive notebooks.  
  Source: [docs.marimo.io/guides/expensive_notebooks](https://docs.marimo.io/guides/expensive_notebooks/) | Strength: **HIGH**

- Tools to prevent unwanted re-runs: `mo.stop(condition)`, disable individual cells, disable autorun on startup, disable autorun on cell execution.  
  Source: [docs.marimo.io/guides/expensive_notebooks](https://docs.marimo.io/guides/expensive_notebooks/) | Strength: **HIGH**

### Running notebooks as plain Python scripts

- Full support: `python my_notebook.py` executes linearly — no reactive engine, no DAG. Standard Python execution semantics.  
  Source: [docs.marimo.io/guides/scripts](https://docs.marimo.io/guides/scripts/) | Strength: **HIGH**

- Scheduler tools (cron, Airflow, Prefect) explicitly supported for marimo notebooks run as scripts.  
  Source: [docs.marimo.io/guides/scripts](https://docs.marimo.io/guides/scripts/) | Strength: **HIGH**

- Your training script can be structured as a marimo notebook but invoked as `python notebook.py &` for non-reactive execution — IF shell access is available (see Section 2, UNKNOWN).

### Subprocess launching patterns

- marimo docs do **NOT** provide an explicit pattern for launching detached subprocesses. The expensive notebooks guide covers only: `mo.stop`, disabling autorun, disabling individual cells.  
  Source: [docs.marimo.io/guides/expensive_notebooks](https://docs.marimo.io/guides/expensive_notebooks/) | Strength: **HIGH** (documented absence)

- Within a cell, `subprocess.Popen(...)` should work and won't be interrupted by reactivity mid-execution. Whether the subprocess outlives the cell's completion and whether molab's sandbox kills it on session expiry is **UNKNOWN.**

---

## Section 8 — Data Ingress/Egress

### What is documented

- **UI upload only** (confirmed): "From here you can upload additional data files" via the file tree sidebar.  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH**  
  Impractical for 100 GB.

- **GitHub notebook mirroring** (confirmed): notebooks can be synced from GitHub. Covers code only, not large binary data.  
  Source: [docs.marimo.io/guides/molab](https://docs.marimo.io/guides/molab/) | Strength: **HIGH**

- **Google Drive integration** and "streamlined local-to-remote-and-back development workflow" listed as **future/coming features**, not currently available.  
  Source: [marimo.io/blog/reintroducing-molab](https://marimo.io/blog/reintroducing-molab) | Strength: **HIGH**

### What is NOT documented

- `rclone`, `rsync`, `wget`, `curl` CLI access in the molab environment: **UNKNOWN**
- Whether molab exposes R2 bucket credentials/endpoint for direct `rclone copy` seeding: **UNKNOWN**
- `git-lfs` support: **UNKNOWN**
- Bandwidth caps: **NOT DOCUMENTED**

**Practical implication:** Seeding 50–150 GB of model weights and covariance caches has **no documented path** in molab. Browser-based upload is the only confirmed method, which is impractical at that scale. This is a **second decisive blocker** after storage quota.

---

## Section 9 — Alternatives Comparison

| Platform | Persistent Storage | Multi-hour Unattended GPU | CLI Agent / Shell | Pinned Env | Best GPU (free) | Cost |
|---|---|---|---|---|---|---|
| **molab (free)** | "Limited" per-notebook on R2 (quota UNKNOWN; likely << 50 GB); object API, not POSIX | 12h session max; 90-min idle kill; background process survival UNKNOWN | Claude Code via marimo-pair (routes through notebook cells, not detached shell) | uv-based; reproducible env "coming soon"; no sudo/apt confirmed | RTX Pro 6000 96 GB | Free; "reasonable use" undefined |
| **Google Colab Free** | None (100 GB ephemeral, wiped on disconnect) | ~12h session, ~90-min idle, no background survival | No persistent terminal | pip; apt via `!apt-get`; no sudo | T4 16 GB (not guaranteed) | Free |
| **Google Colab Pro+ ($49.99/mo)** | ~50–100 GB via Google Drive mount (POSIX via FUSE) | Same session limits; still killed on disconnect | Limited | pip + apt | A100 40 GB (sometimes) | $49.99/mo |
| **Kaggle Free** | ~20 GB `/kaggle/working/` POSIX, persistent | 12h session; 30 GPU-hrs/week cap; no background survival | No terminal; notebook cells only | pip; no sudo | P100 16 GB | Free |
| **Lightning AI Free** | 50–100 GB POSIX persistent, survives sessions | 4-hr idle restart; ~80 GPU-hrs/month on spot; jobs survive if Studio running | SSH access, VS Code, full bash terminal; can run nohup/tmux | pip, conda, apt; full env control | T4/L4/A10G/L40S (16–48 GB VRAM) | Free (~80 spot-GPU-hrs/mo) |
| **Modal Starter (free)** | 1 TiB free persistent volumes — POSIX-like network volumes | No inherent session limit; functions run until done; fits unattended jobs | CLI + Python SDK; arbitrary subprocess OK | pip; Docker containers; full env control | RTX Pro 6000 at ~$3.03/hr | $30/mo free credits (~10h RTX Pro 6000) |
| **RunPod (current)** | Persistent network volumes; full POSIX; configurable 50–500+ GB | No session limit; pods run until stopped; nohup/setsid/tmux all work | Full root SSH shell; any CLI | Full Docker/pip/apt/conda | RTX 4090 24 GB (~$0.69/hr spot) | ~$0.69–$0.74/hr spot |

**Sources:** Lightning AI: [usagepricing.com/blueprint/lightning-ai](https://www.usagepricing.com/blueprint/lightning-ai), [gmicloud.ai free GPU guide](https://www.gmicloud.ai/ja/blog/best-free-gpu-cloud-options-for-ai-startups-and-researchers) | Modal: [modal.com/pricing](https://modal.com/pricing), [usagepricing.com/blueprint/modal](https://www.usagepricing.com/blueprint/modal) | Kaggle: [deepwiki.com kaggle GPU session management](https://deepwiki.com/hoang-quoc-trung/remote-ssh-kaggle-vscode/6.1-gpu-usage-and-session-management) | Colab: [medium.com/data-science-in-your-pocket colab free GPU](https://medium.com/data-science-in-your-pocket/understanding-google-colab-free-gpu-in-detail-15074081d494)

---

## UNKNOWN — Requires Direct Test on molab

The following cannot be resolved from documentation and require hands-on experimentation (each ~5–15 minutes):

1. **Storage quota per notebook:** Write files totaling 10 GB, 50 GB, 100 GB. Record where it fails or if quota is enforced.
2. **Storage POSIX vs object API:** Check whether `~` or a mount path is accessible via `open()`, `os.listdir()`, `numpy.save()`, `torch.save()` — or whether it requires boto3/S3 calls.
3. **HF cache location:** Run `import os; print(os.environ.get('HF_HOME', '~/.cache/huggingface'))` and check whether that path is on persistent R2-backed storage or ephemeral local disk.
4. **PyTorch version pre-installed:** `import torch; print(torch.__version__)` — verify ≥2.7.0+cu128 for sm_120 support.
5. **CUDA/driver version:** `!nvidia-smi` — confirm driver ≥ R570, CUDA 12.8.
6. **Shell/terminal access:** Whether a raw bash terminal tab is available. Try: `import subprocess; r = subprocess.run(['bash', '-c', 'which tmux && tmux --version'], capture_output=True); print(r.stdout.decode())`
7. **Background process survival past idle timeout:** Launch `subprocess.Popen(['sleep', '7200'])`, close the browser for 91+ minutes, reopen. Is the process alive?
8. **nohup/setsid survival of browser disconnect:** If a terminal exists, run `setsid python -c "import time; time.sleep(7200)" &`, disconnect, reconnect after >90 min. Still running?
9. **Internet egress for HuggingFace gated models:** `HF_TOKEN=<token> python -c "from huggingface_hub import snapshot_download; snapshot_download('meta-llama/Llama-3.2-3B-Instruct')"` — does authentication work and does the download complete?
10. **Data ingress at scale:** Whether `wget`, `curl`, or `rclone` are available in-environment; whether R2 bucket credentials are exposed for direct seeding.
11. **sudo/apt-get availability:** `sudo apt-get install tmux` — does it work?

---

## Go / No-Go Bottom Line

### (a) Hold 50–150 GB of persistent caches across sessions

**LIKELY NO** based on current documentation. The official description is "a limited amount of persistent storage per notebook" backed by R2. No quota is published; Cloudflare R2's own free tier is only 10 GB/month. The framing "limited" strongly suggests it is well below 50 GB. Even if quota were sufficient, R2 is an object store, not a POSIX filesystem — all existing file I/O code would need rewriting unless molab presents it as a mounted path (undocumented).

**Decisive blocker unless UNKNOWN items 1–2 resolve favorably.**

### (b) Run multi-hour unattended detached jobs surviving idle/session limits

**LIKELY NO.** The 90-minute idle shutdown applies to the entire CoreWeave sandbox. Background processes (nohup/setsid) almost certainly die with the sandbox. The marimo-pair / Claude Code integration routes all execution through notebook cells, not a detached shell. There is no documented mechanism for "detached from browser" long-running jobs comparable to the current RunPod workflow.

**Decisive blocker unless UNKNOWN items 7–8 resolve unexpectedly favorably.**

### (c) Run the Claude Code CLI with arbitrary pip/git

**PARTIALLY SUPPORTED.** marimo-pair officially supports Claude Code as an agent, but it operates by writing notebook cells — not as a free-roaming terminal agent executing arbitrary shell commands. Whether a full bash terminal with pip, git, apt, and Claude Code CLI is available directly is undocumented. uv-based package installs appear supported; root/sudo is UNKNOWN.

**Conditional: requires UNKNOWN items 6, 11 testing.**

### (d) Run Blackwell sm_120 + stock PyTorch fp16 editing

**LIKELY YES, with caveats.** The RTX Pro 6000 Blackwell is CC 12.0 and PyTorch 2.7.0+cu128 includes sm_120 support (confirmed live). The pre-installed torch version is undocumented — if it is pre-2.7.0, you will hit "no kernel image" errors, but reinstalling via uv should fix this. However, your MEMIT weight-editing determinism baselines from the RTX 4090 (Ada, CC 8.9) will **not be bit-identical on Blackwell (CC 12.0)** — fp16 matmul reduction order differs across GPU architectures per PyTorch's own documentation. **All determinism gates must be re-baselined on Blackwell from scratch.**

**Conditional on torch version; determinism re-baseline required.**

### Overall Recommendation

**Do not migrate your primary research workflow to molab's free tier** without first running the minimal experiments in the UNKNOWN list — specifically items 1 (quota), 2 (POSIX mount), 7 (idle survival), and 8 (detached job survival). All four go/no-go criteria have at least one decisive open question resolvable only by a 30-minute hands-on test. If any of items 1/2/7/8 fail as expected from current evidence, molab is not viable for this workload today.

**RunPod (current setup) or Modal (for unattended GPU jobs with persistent volumes) remains the correct choice for production research.** molab's RTX Pro 6000 96 GB VRAM is by far the best GPU in the free-tier set, and warrants testing — but only as a supplement once the blockers are characterized, not as a primary migration target.

---

## Source Index

| Source | URL | Strength |
|---|---|---|
| molab official docs | https://docs.marimo.io/guides/molab/ | HIGH |
| molab reintroduction blog post | https://marimo.io/blog/reintroducing-molab | HIGH |
| molab announcement blog post | https://marimo.io/blog/announcing-molab | HIGH |
| marimo agent CLI guide (marimo-pair) | https://docs.marimo.io/guides/generate_with_ai/marimo_pair/ | HIGH |
| marimo scripts guide | https://docs.marimo.io/guides/scripts/ | HIGH |
| marimo reactivity guide | https://docs.marimo.io/guides/reactivity/ | HIGH |
| marimo expensive notebooks guide | https://docs.marimo.io/guides/expensive_notebooks/ | HIGH |
| Cloudflare R2 pricing | https://developers.cloudflare.com/r2/pricing/ | HIGH |
| Cloudflare R2 limits | https://developers.cloudflare.com/r2/platform/limits/ | HIGH |
| NVIDIA RTX PRO 6000 Blackwell spec sheet (PDF) | https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/rtx-pro-6000-blackwell-workstation-edition/workstation-blackwell-rtx-pro-6000-workstation-edition-nvidia-us-3519208-web.pdf | HIGH |
| NVIDIA CUDA GPU compute capability list | https://developer.nvidia.com/cuda/gpus | HIGH |
| NVIDIA Blackwell compatibility guide | https://docs.nvidia.com/cuda/blackwell-compatibility-guide/ | HIGH |
| NVIDIA Blackwell tuning guide | https://docs.nvidia.com/cuda/blackwell-tuning-guide/index.html | HIGH |
| NVIDIA CUDA/PyTorch Blackwell migration guide | https://forums.developer.nvidia.com/t/software-migration-guide-for-nvidia-blackwell-rtx-gpus-a-guide-to-cuda-12-8-pytorch-tensorrt-and-llama-cpp/321330 | HIGH |
| NVIDIA Blackwell/CUDA 12.9 architecture blog | https://developer.nvidia.com/blog/nvidia-blackwell-and-nvidia-cuda-12-9-introduce-family-specific-architecture-features/ | HIGH |
| PyTorch reproducibility docs | https://pytorch.org/docs/stable/notes/randomness.html | HIGH |
| PyTorch issue #157549 (sm_120 RTX Pro 6000 live test) | https://github.com/pytorch/pytorch/issues/157549 | HIGH |
| PyTorch forum: sm_120 support for RTX 5060 | https://discuss.pytorch.org/t/pytorch-support-for-sm-120-nvidia-geforce-rtx-5060/220941 | HIGH |
| PyTorch forum: CUDA error RTX Pro 6000 | https://discuss.pytorch.org/t/pyrtorch-cuda-error-with-nvidia-blackwell-rtx-pro-6000/223534 | MEDIUM |
| PyTorch forum: different result on different GPU | https://discuss.pytorch.org/t/different-result-on-different-gpu/102502 | MEDIUM |
| BIZON RTX Pro 6000 specs | https://bizon-tech.com/blog/new-rtx-pro-6000-blackwell-gpus-tech-specs | HIGH |
| HN: molab announcement | https://news.ycombinator.com/item?id=44608312 | MEDIUM |
| Lightning AI pricing analysis | https://www.usagepricing.com/blueprint/lightning-ai | MEDIUM |
| Modal pricing | https://modal.com/pricing | HIGH |
| Modal pricing analysis | https://www.usagepricing.com/blueprint/modal | MEDIUM |
| Kaggle GPU session management | https://deepwiki.com/hoang-quoc-trung/remote-ssh-kaggle-vscode/6.1-gpu-usage-and-session-management | MEDIUM |
| GMI Cloud free GPU guide | https://www.gmicloud.ai/ja/blog/best-free-gpu-cloud-options-for-ai-startups-and-researchers | MEDIUM |
| Google Colab free GPU overview | https://medium.com/data-science-in-your-pocket/understanding-google-colab-free-gpu-in-detail-15074081d494 | MEDIUM |

---

*Report compiled June 17, 2026. All claims derive from primary sources or explicitly labeled inference. Claims marked UNKNOWN require direct empirical testing on molab.*
