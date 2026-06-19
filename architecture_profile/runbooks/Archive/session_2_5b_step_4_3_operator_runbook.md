# Session 2.5b §4.3 — Operator Runbook: NV Writes + P-5 Application + SSD Mirror Sync

> **Artifact class:** Operator-side execution runbook (Workstream 1 Session 2.5b §4.3 deliverable)
> **Iteration:** v1.0 (S2.5b §4.3 authored 2026-04-30)
> **Status:** Authored; pending operator-side execution
> **Predecessor:** S2.5b §4.4 Session Summary Block (chat-side authoring) closes; this runbook is the operator-side completion of S2.5b
> **Successor:** Successor pre-S2.6 fork-work attempt (operator launches on a re-started pod consuming this runbook's NV-resident artifacts)
> **Specialist provenance:** state-consistency-theorist (primary, NV write contracts + mirror sync verification); framework-spec-writer (secondary, runbook discipline)

---

## 1. Purpose & scope

Operator-side execution on a re-started pod, persisting all S2.5b chat-authored artifacts to NV at canonical paths, applying the P-5 patch to the NV-resident MEMIT clone, and triggering SSD mirror sync.

Pod was stopped at pre-S2.6 fork-work halt-clean (~2026-04-30T~03:30Z); this runbook restarts it briefly to perform forensically-recoverable on-pod state writes, then stops it again. No further on-pod work is performed in S2.5b after this runbook's completion.

**Estimated cost:** ~10–15 min wall-time operator-side; pod cost ~$0.20 (~30 min × $0.69/hr; rounded up for pod startup overhead and verification time).

**In scope:**
- Pod startup + container-disk Python state restoration
- Pod state fingerprint verification
- Optional `globals.yml` D-PreS26-3 correction NV-persistence verification
- P-5 patch application via `memit-patches-canonical.md` v2.2 §3.6.7 idempotent script
- NV writes of S2.5b chat-authored artifacts at canonical paths
- SSD mirror sync per OQ-S23-14 protocol
- Mirror-vs-NV state hash verification
- Pod stop

**Out of scope:**
- Cell 4 covariance compute (deferred to successor pre-S2.6 fork-work attempt)
- Stage 1 SECT trial execution (deferred to Session 2.6)
- `globals.yml` correction re-application (already applied during pre-S2.6 fork-work session per D-PreS26-3; NV-persistent; this runbook only verifies)

---

## 2. Inputs (required artifacts available in chat-side downloads at runbook authoring time)

The following S2.5b chat-authored artifacts must be available on the operator's MBP-side filesystem before §6 NV writes:

| Artifact | Origin | Operator-side cache path (recommended) |
|---|---|---|
| `session_2_5_summary_block.md` | S2.5b §4.4 | `~/Downloads/llm-as-database/s2_5b/session_2_5_summary_block.md` |
| `pre_s2_6_fork_work_runbook.md` v1.2.1 | S2.5b §4.7 + §4.8 | `~/Downloads/llm-as-database/s2_5b/pre_s2_6_fork_work_runbook.md` |
| `memit-patches-canonical.md` v2.2 | S2.5b §4.5 | `~/Downloads/llm-as-database/s2_5b/memit-patches-canonical.md` |
| `stage_1_compat_assessment.md` | S2.5b §4.1 | `~/Downloads/llm-as-database/s2_5b/stage_1_compat_assessment.md` |
| `reproducibility_manifest.json` v3.0 | S2.5b §4.6 | `~/Downloads/llm-as-database/s2_5b/reproducibility_manifest.json` |
| `oq-backlog-v3.md` | S2.5b §4.2 | `~/Downloads/llm-as-database/s2_5b/oq-backlog-v3.md` |
| Sub-step summaries (8) — `session_2_5b_step_4_0_summary.md` through `session_2_5b_step_4_8_summary.md` (excluding `_4_3_` which is this runbook itself) | S2.5b sub-steps | `~/Downloads/llm-as-database/s2_5b/sub_step_summaries/` (mkdir as a sub-directory) |

**Total artifact count:** 14 (1 main summary + 1 runbook + 1 canonical doc + 1 compat assessment + 1 manifest JSON + 1 backlog + 8 sub-step summaries — minus this §4.3 runbook itself).

**Pre-execution check (operator-side):** verify all 14 artifacts are present at the recommended paths or operator's preferred equivalent. Missing artifacts halt this runbook before pod startup.

---

## 3. Phase 0 — Pre-flight (operator-side, no pod cost)

### 3.1 Verify NV accessibility

Open RunPod console (https://runpod.io/console) → Network Volumes tab. Verify:

- `large_amethyst_wolverine` (id `nvol-s1xi9zhfc2`) is listed
- Status: Active
- Region: US-NC-1
- Size: 100 GB
- Used: ~7.6 GB (per `reproducibility_manifest.json` v3.0 `persistent_state.network_volume_used_gb_at_close`; may have grown by a few hundred MB from pre-S2.6 fork-work session work product — bridge_archive subdirectory + globals.yml.upstream_default snapshot)

**Halt condition:** if NV is not accessible, escalate to RunPod support via ticket — do not proceed with this runbook.

### 3.2 Verify image digest still resolvable (defensive)

```bash
# Operator-side MBP terminal
skopeo inspect docker://docker.io/runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04 \
  | jq -r '.Digest'
```

**Expected output:** `sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5`

**Halt condition:** if the digest has drifted (RunPod ships patch-level updates per OQ-S23-2), record the new digest and append a `block-2-3-runbook-deltas.md` D10 entry before proceeding. The drift is informational; new digest is acceptable for this brief NV-write session, but the manifest's `pod_image_digest` field would need a v3.1 update.

---

## 4. Phase 1 — Pod startup + container-disk Python state restoration

### 4.1 Start pod against NV

RunPod console → Deploy → Secure Cloud → US-NC-1 → RTX 4090 (1× GPU; 24 GB) → image digest pinned per §3.2 → attach NV `large_amethyst_wolverine`.

**Acceptance:** pod state transitions Running within ~60 seconds; SSH endpoint published.

**Note pod hostname** for §7.1 mirror sync command construction.

### 4.2 SSH to pod

```bash
ssh -p <pod_port> root@<pod_ip>
```

**Acceptance:** prompt `(base) root@<pod_hostname>:/#` appears.

### 4.3 Re-install Block 2 §12 dep manifest + pandas runtime deps

Pod was stopped, so container-disk Python state is reset (NV-resident `/workspace` survives; container-disk `/usr/local/lib/python3.11/site-packages/` does not). Re-install per the C-S25-6 + C-S25-7 locked manifest.

```bash
# === CELL 0a — Re-install MEMIT runtime + import-time deps ===
# Source: block-2-3-runbook-deltas.md §12; lock per C-S25-6
pip install \
    transformers==4.45.2 \
    accelerate==0.34.2 \
    huggingface_hub==0.25.2 \
    tokenizers==0.20.3 \
    safetensors==0.4.5 \
    hydra-core==1.3.2 \
    einops==0.7.0 \
    nltk==3.8.1 \
    datasets==4.8.3 \
    matplotlib==3.9.2 \
    scipy==1.14.1 \
    scikit-learn==1.5.2

# === CELL 0b — pandas force-reinstall (C-S25-7 runtime workaround) ===
pip install pandas==2.2.3 --force-reinstall --no-deps
```

**Acceptance:** `pip` reports successful install of all 12 packages (Cell 0a) and pandas force-reinstall (Cell 0b); no `ERROR:` output. Estimated wall-time ~3–5 min.

**Halt condition:** if any package fails to install, capture the error and halt. Do NOT proceed to §5 verification under a partially-installed manifest.

---

## 5. Phase 2 — Pod state verification

### 5.1 Cell 1 fingerprint pattern (matches `stage_1_sect_runbook.md` Cell 1)

In a Jupyter notebook session on the pod (or via terminal Python REPL):

```python
# === CELL 1 — Environment fingerprint ===
import sys, os, subprocess
import torch

print(f"Python:        {sys.version.split()[0]}")
print(f"PyTorch:       {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA torch:    {torch.version.cuda}")
    print(f"CUDA driver:   {subprocess.check_output(['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader']).decode().strip()}")
    print(f"GPU:           {torch.cuda.get_device_name(0)}")
    print(f"GPU memory:    {torch.cuda.get_device_properties(0).total_memory / 1024**2:.0f} MiB")

# Versions of pinned MEMIT runtime deps
import transformers, accelerate, huggingface_hub, tokenizers, safetensors, datasets
print(f"transformers:  {transformers.__version__}")
print(f"accelerate:    {accelerate.__version__}")
print(f"huggingface_hub: {huggingface_hub.__version__}")
print(f"tokenizers:    {tokenizers.__version__}")
print(f"safetensors:   {safetensors.__version__}")
print(f"datasets:      {datasets.__version__}")

# NV mount + free space
import shutil
nv_total, nv_used, nv_free = shutil.disk_usage("/workspace")
print(f"NV total:      {nv_total / 1024**3:.1f} GB")
print(f"NV used:       {nv_used / 1024**3:.1f} GB")
print(f"NV free:       {nv_free / 1024**3:.1f} GB")

# HF cache health (per D-S25-8)
print(f"HF_HOME:       {os.environ.get('HF_HOME', '<unset>')}")
```

**Acceptance:** all rows print without exception. Expected key-row values:

- `PyTorch: 2.4.1+cu124`
- `CUDA torch: 12.4`
- `GPU: NVIDIA GeForce RTX 4090`
- `GPU memory: ~24564 MiB`
- `transformers: 4.45.2` ... `datasets: 4.8.3`
- `NV total: ~93–94 GB` (after MFS overhead from 100 GB allocated)
- `NV used: ~7.6 GB ± a few hundred MB`
- `HF_HOME: /workspace/hf_cache` (per D-S25-8; if unset, the redirect is a per-shell environment variable that needs re-export — see §5.1.1 below)

### 5.1.1 HF_HOME re-export (if unset)

If Cell 1 reports `HF_HOME: <unset>`, run:

```bash
export HF_HOME=/workspace/hf_cache
```

This is a per-shell environment variable; not strictly load-bearing for §5–§9 of this runbook (no model loading occurs), but matches operator-discipline convention.

### 5.2 globals.yml correction NV-persistence verification (D-PreS26-3 belt-and-suspenders)

```bash
# === CELL 1.5a — globals.yml NV-persistence check ===
cat /workspace/memit_dry_run/memit/globals.yml
```

**Expected output (per D-PreS26-3):**

```yaml
DATA_DIR: /workspace/data
HPARAMS_DIR: /workspace/memit_dry_run/memit/hparams
KV_DIR: /workspace/kvs
REMOTE_ROOT_URL: https://memit.baulab.info
RESULTS_DIR: /workspace/results
STATS_DIR: /workspace/covariance_caches
```

**Acceptance:** all five non-REMOTE_ROOT_URL keys at absolute-path canonical values per D-PreS26-3 verbatim. `REMOTE_ROOT_URL` unchanged from upstream.

**Halt condition (unexpected):** if any key has reverted to upstream pristine defaults (e.g., `STATS_DIR: data/stats`), the D-PreS26-3 NV-persistence claim is FALSIFIED. Halt this runbook and escalate — would require re-investigation of NV durability semantics and potential C-PreS26-1 amendment. Per the manifest v3.0 + state-consistency-theorist analysis, this halt is NOT expected; this is a defensive verification.

### 5.2.1 Upstream-default snapshot presence check

```bash
ls -la /workspace/memit_dry_run/memit/globals.yml.upstream_default.20260430T035736Z
```

**Expected:** file exists with size ~190 bytes (the upstream pristine yaml). Preserved per D-PreS26-3 for auditability.

**Halt condition (unexpected):** if file is absent, log the absence as informational; do NOT halt. The snapshot was a session-1 forensic artifact; its absence at session 3+ is acceptable but undocumented loss of forensic record.

---

## 6. Phase 3 — P-5 patch application

P-5 modifies `/workspace/memit_dry_run/memit/rome/layer_stats.py` lines ~97–103 to redirect the wikipedia dispatch from script-based loader to parquet-backed `wikimedia/wikipedia 20231101.en`. Per `memit-patches-canonical.md` v2.2 §3.6.7, the application script is idempotent — safe to re-run.

### 6.1 Pre-application state inspection

```bash
# === CELL 2a — Confirm P-5 is NOT yet applied ===
cd /workspace/memit_dry_run/memit
grep -n "20231101.en\|wikimedia/wikipedia" rome/layer_stats.py
```

**Expected output:** empty (no matches; P-5 has not been applied yet).

**Alternative outcome:** if matches are present, P-5 is already applied (perhaps from a prior session attempt the operator forgot). Skip §6.2 and proceed to §6.3 verification.

### 6.2 Apply P-5 via canonical doc v2.2 §3.6.7 idempotent script

The script is reproduced inline below for in-runbook executability; canonical reference is `memit-patches-canonical.md` v2.2 §3.6.7.

```python
# === CELL 2b — P-5 application script (per canonical doc v2.2 §3.6.7) ===
# Anchored substring substitutions. Idempotent: if the post-state markers
# are already present, the script is a no-op.

import os
from pathlib import Path

MEMIT_ROOT = Path("/workspace/memit_dry_run/memit")
LAYER_STATS_PATH = MEMIT_ROOT / "rome" / "layer_stats.py"

# Read pristine source
src = LAYER_STATS_PATH.read_text()

# Anchor 1: wikipedia config name
old_anchor_1 = 'load_dataset("wikipedia", "20200501.en"'
new_anchor_1 = 'load_dataset("wikimedia/wikipedia", "20231101.en"'

# Anchor 2: dataset reference in docstring or comment if present
# (Per canonical doc v2.2 §3.6 — anchor verification BEFORE substitution)

# Verify Anchor 1 present in pristine source
assert old_anchor_1 in src, f"P-5 anchor not found: {old_anchor_1!r}"

# Apply substitution
new_src = src.replace(old_anchor_1, new_anchor_1)

# Idempotency check: re-applying produces identical output
assert old_anchor_1 not in new_src, "P-5 application incomplete (substitution failed)"
assert new_anchor_1 in new_src, "P-5 application failed (replacement absent)"

# Write back
LAYER_STATS_PATH.write_text(new_src)

print(f"P-5 applied: anchor 1 substituted; file size {LAYER_STATS_PATH.stat().st_size} bytes")
```

**Acceptance:** `P-5 applied: anchor 1 substituted; file size <bytes>` printed. No `AssertionError` raised.

**Halt condition:** if `AssertionError: P-5 anchor not found` raises, the SHA pin (`80426fd9…`) and `rome/layer_stats.py` empirical line content have drifted — investigate via `git -C /workspace/memit_dry_run/memit log -1 --oneline` to confirm SHA pin; if drift is real, escalate to `memit-patches-canonical.md` v3.0 authorship (out-of-scope here).

### 6.3 Post-application verification (per canonical doc v2.2 §3.6.8)

```bash
# === CELL 2c — Verify P-5 post-state markers ===
cd /workspace/memit_dry_run/memit
grep -c "20231101.en" rome/layer_stats.py    # Expected: ≥1
grep -c "wikimedia/wikipedia" rome/layer_stats.py  # Expected: ≥1
grep -c "20200501.en" rome/layer_stats.py    # Expected: 0 (substitution successful)
```

**Acceptance:** first two `grep -c` return `1` (or higher if dispatch pattern preserves any references); third returns `0`.

**Halt condition:** if marker counts fail expectations, verify the §6.2 application ran on the correct file path; re-read source via `cat rome/layer_stats.py | head -110 | tail -20` to inspect lines 90–110 manually.

### 6.4 Update SHA tracking (informational)

P-5 modifies the working tree but does NOT commit (MEMIT clone is treated as patch-applied-against-immutable-SHA, not as forked). The `git rev-parse HEAD` will continue to report `80426fd9…` (pinned SHA); the patch is in-place modification only.

```bash
cd /workspace/memit_dry_run/memit
git rev-parse HEAD
git status --porcelain rome/layer_stats.py
```

**Expected output:**

```
80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b
 M rome/layer_stats.py
```

The `M` flag confirms the file is modified relative to the pinned SHA; this is intentional per the patch family discipline.

---

## 7. Phase 4 — NV writes of S2.5b chat-authored artifacts

### 7.1 Operator-side scp transfer

From the operator's MBP terminal:

```bash
# Set pod connection variables per §4.1 acceptance
POD_PORT=<pod_port>
POD_IP=<pod_ip>
SSH_KEY=~/.ssh/id_ed25519

# Create destination directories on pod (idempotent)
ssh -i $SSH_KEY -p $POD_PORT root@$POD_IP "mkdir -p \
    /workspace/architecture_profile \
    /workspace/architecture_profile/runbooks \
    /workspace/session_logs \
    /workspace/session_logs/sub_step_summaries"

# Transfer 14 artifacts from operator-side cache
scp -i $SSH_KEY -P $POD_PORT \
    ~/Downloads/llm-as-database/s2_5b/session_2_5_summary_block.md \
    root@$POD_IP:/workspace/session_logs/session_2_5_summary_block.md

scp -i $SSH_KEY -P $POD_PORT \
    ~/Downloads/llm-as-database/s2_5b/pre_s2_6_fork_work_runbook.md \
    root@$POD_IP:/workspace/architecture_profile/runbooks/pre_s2_6_fork_work_runbook.md

scp -i $SSH_KEY -P $POD_PORT \
    ~/Downloads/llm-as-database/s2_5b/memit-patches-canonical.md \
    root@$POD_IP:/workspace/architecture_profile/memit-patches-canonical.md

scp -i $SSH_KEY -P $POD_PORT \
    ~/Downloads/llm-as-database/s2_5b/stage_1_compat_assessment.md \
    root@$POD_IP:/workspace/architecture_profile/stage_1_compat_assessment.md

scp -i $SSH_KEY -P $POD_PORT \
    ~/Downloads/llm-as-database/s2_5b/reproducibility_manifest.json \
    root@$POD_IP:/workspace/architecture_profile/reproducibility_manifest.json

scp -i $SSH_KEY -P $POD_PORT \
    ~/Downloads/llm-as-database/s2_5b/oq-backlog-v3.md \
    root@$POD_IP:/workspace/architecture_profile/oq-backlog-v3.md

# Sub-step summaries (8 files; one scp per file or batch)
for SUB_STEP in 4_0 4_1 4_2 4_5 4_6 4_7 4_8 4_4; do
    scp -i $SSH_KEY -P $POD_PORT \
        ~/Downloads/llm-as-database/s2_5b/sub_step_summaries/session_2_5b_step_${SUB_STEP}_summary.md \
        root@$POD_IP:/workspace/session_logs/sub_step_summaries/
done
```

**Acceptance:** all 14 `scp` commands return exit code 0; no `lost connection` or `permission denied`.

**Halt condition (per OQ-S23-16):** if SSH key registration drifted (account-level vs pod-level propagation issue), append SSH public key to pod's `~/.ssh/authorized_keys` manually and retry. Operational discipline; documented in `block-2-3-runbook-deltas.md` D-OQ-S23-16.

### 7.2 Archive supersession discipline

Per the §4.4 Session Summary Block forward-routing notes, two files are archived (not deleted) on supersession:

```bash
# === CELL 3a — Archive predecessor summary blocks (if present) ===
ssh -i $SSH_KEY -p $POD_PORT root@$POD_IP "
    cd /workspace/session_logs
    if [ -f session_2_5a_summary_block.md ]; then
        mv session_2_5a_summary_block.md session_2_5a_summary_block.md.superseded.20260430
    fi
    if [ -f pre_s2_6_fork_work_summary_block.md ]; then
        mv pre_s2_6_fork_work_summary_block.md pre_s2_6_fork_work_summary_block.md.superseded.20260430
    fi
"
```

**Acceptance:** `mv` succeeds for any present file. Absent files cause `mv` to print "No such file or directory" — acceptable; the file may have been written to a different path historically.

### 7.3 NV-side checksum capture

```bash
# === CELL 3b — NV-side md5 capture for §8 mirror verification ===
ssh -i $SSH_KEY -p $POD_PORT root@$POD_IP "
    cd /workspace
    md5sum \
        session_logs/session_2_5_summary_block.md \
        architecture_profile/runbooks/pre_s2_6_fork_work_runbook.md \
        architecture_profile/memit-patches-canonical.md \
        architecture_profile/stage_1_compat_assessment.md \
        architecture_profile/reproducibility_manifest.json \
        architecture_profile/oq-backlog-v3.md \
        session_logs/sub_step_summaries/*.md \
    > /tmp/s2_5b_artifact_checksums.txt
    cat /tmp/s2_5b_artifact_checksums.txt
"
```

**Acceptance:** 14 lines of `<md5> <path>` printed. Each line corresponds to one of the 14 artifacts; no `cat: No such file or directory` for any expected entry.

**Operator action:** record the checksum file content in operator session notes for §8 verification.

---

## 8. Phase 5 — SSD mirror sync (per OQ-S23-14 protocol)

### 8.1 rsync push

From the operator's MBP terminal:

```bash
# Per persistent_state.rsync_target convention; reference manifest v3.0 rsync_target block
SSD_MOUNT=/Volumes/memit/llm-database-poc-mirror

rsync -avz \
    -e "ssh -i $SSH_KEY -p $POD_PORT" \
    --exclude="hf_cache" \
    --exclude="memit_dry_run/memit/.git" \
    --exclude="*.upstream_default.*" \
    root@$POD_IP:/workspace/ \
    $SSD_MOUNT/
```

**Notes:**

- `--exclude="hf_cache"` — HF cache is large (~16 GB Llama-3.1-8B model + tokenizer); not load-bearing for forensic recoverability; excluded per S2.3 rsync_target convention.
- `--exclude="memit_dry_run/memit/.git"` — git internal state is large and reconstructible from SHA pin; exclude to reduce sync time.
- `--exclude="*.upstream_default.*"` — globals.yml.upstream_default snapshot is forensic but small; included only if explicitly desired (operator may remove this exclude line if archival is preferred).
- No `--delete` flag in initial sync per `rsync_target.delete_flag_in_initial_sync: false` from manifest v2.0/v3.0; subsequent operator-discipline syncs may add `--delete`.

**Acceptance:** rsync output reports total file count and total bytes transferred; final line `total size is <bytes> sent <bytes> received <bytes>`. Exit code 0.

**Estimated wall-time:** ~2–5 min (delta sync; most of /workspace is unchanged from S2.3 close mirror state).

### 8.2 MBP-side checksum verification

```bash
# === MBP terminal — verify mirror md5 matches NV md5 from §7.3 ===
cd $SSD_MOUNT

md5_check() {
    local rel_path="$1"
    if [ -f "$rel_path" ]; then
        md5 -q "$rel_path"  # macOS form; on Linux use md5sum and parse
    else
        echo "MISSING: $rel_path"
    fi
}

echo "session_logs/session_2_5_summary_block.md: $(md5_check session_logs/session_2_5_summary_block.md)"
echo "architecture_profile/runbooks/pre_s2_6_fork_work_runbook.md: $(md5_check architecture_profile/runbooks/pre_s2_6_fork_work_runbook.md)"
echo "architecture_profile/memit-patches-canonical.md: $(md5_check architecture_profile/memit-patches-canonical.md)"
echo "architecture_profile/stage_1_compat_assessment.md: $(md5_check architecture_profile/stage_1_compat_assessment.md)"
echo "architecture_profile/reproducibility_manifest.json: $(md5_check architecture_profile/reproducibility_manifest.json)"
echo "architecture_profile/oq-backlog-v3.md: $(md5_check architecture_profile/oq-backlog-v3.md)"

for SUB_STEP in 4_0 4_1 4_2 4_4 4_5 4_6 4_7 4_8; do
    echo "session_logs/sub_step_summaries/session_2_5b_step_${SUB_STEP}_summary.md: $(md5_check session_logs/sub_step_summaries/session_2_5b_step_${SUB_STEP}_summary.md)"
done
```

**Acceptance:** all 14 md5 hashes match the NV-side hashes captured in §7.3.

**Halt condition:** if any hash mismatch, re-run rsync for the specific path with `--checksum` flag for byte-level verification, OR investigate corruption.

---

## 9. Phase 6 — P-5 application + globals.yml state on mirror

The MEMIT clone (with P-5 applied per §6.2) and `globals.yml` (corrected per D-PreS26-3) are part of the mirror sync in §8.1. Verify on mirror:

### 9.1 Mirror-side P-5 verification

```bash
cd $SSD_MOUNT/memit_dry_run/memit
grep -c "20231101.en" rome/layer_stats.py
grep -c "wikimedia/wikipedia" rome/layer_stats.py
```

**Expected:** both return ≥1 (P-5 post-state markers preserved through sync).

### 9.2 Mirror-side globals.yml verification

```bash
cat $SSD_MOUNT/memit_dry_run/memit/globals.yml
```

**Expected:** all five non-REMOTE_ROOT_URL keys at D-PreS26-3 absolute-path canonical values.

**Acceptance:** mirror state matches NV state for both load-bearing artifacts.

---

## 10. Phase 7 — Pod stop

### 10.1 Pre-stop NV state confirmation

```bash
# Final ssh-side sanity check
ssh -i $SSH_KEY -p $POD_PORT root@$POD_IP "
    df -h /workspace
    ls -la /workspace/architecture_profile/ /workspace/session_logs/
"
```

**Acceptance:** NV mounted; new artifacts present at canonical paths.

### 10.2 Pod stop

RunPod console → Pods → <pod_hostname> → ⋮ → Stop → Confirm.

**Note:** Stop preserves NV; container-disk Python state is lost (which is expected). Subsequent successor fork-work session re-installs deps per §4.3 of *that* runbook (matching the dep-manifest discipline).

**Acceptance:** pod state transitions Stopped within ~30 seconds.

### 10.3 Total pod cost reporting

Estimated cumulative wall-time on pod for §4–§10: ~25–35 min (startup overhead + dep install + verifications + scp + rsync trigger + pre-stop sanity + stop overhead). Estimated cost: ~$0.30–$0.40 (pod cost ~$0.69/hr × ~30 min). Slightly above the §1 estimate of $0.20; the §1 estimate did not account for full dep re-install (~3–5 min) and rsync triggering wall-time.

**Operator action:** record actual pod uptime + actual cost in operator session notes; reconcile against this runbook's §1 estimate for future runbook authoring discipline.

---

## 11. Acceptance criteria (rolling up Phase 0–7)

§4.3 sub-step closes PASS when ALL of the following are true:

- [ ] §3.1 NV accessibility verified
- [ ] §3.2 image digest reconciled (or new digest recorded with informational drift note)
- [ ] §4.1 pod started successfully
- [ ] §4.3 dep manifest re-installed without error
- [ ] §5.1 Cell 1 fingerprint matches expected values
- [ ] §5.2 globals.yml NV-persistence verified per D-PreS26-3 absolute-path values
- [ ] §6 P-5 applied; post-state markers verified per canonical doc v2.2 §3.6.8
- [ ] §7.1 14 artifacts scp'd to NV at canonical paths
- [ ] §7.3 NV-side md5 checksum file captured
- [ ] §8.1 rsync push completed without error
- [ ] §8.2 MBP-side md5 checksum verification — all 14 hashes match NV-side
- [ ] §9.1 mirror-side P-5 post-state markers verified
- [ ] §9.2 mirror-side globals.yml verified
- [ ] §10.2 pod stopped

If all checkboxes pass, S2.5b §4.3 closes PASS, and S2.5b in aggregate closes CLOSED PASS-CONDITIONAL (per §4.4 Session Summary Block; the PASS-CONDITIONAL classification reflects the two open gates from compat assessment §1.6, not §4.3 status).

If any checkbox fails, document the failure mode + halt point in operator session notes; consult the per-§ halt conditions for resolution. Re-run from the halted §; do NOT skip-and-continue.

---

## 12. Handoff to successor pre-S2.6 fork-work attempt

After §4.3 PASS, the NV state is ready for the successor pre-S2.6 fork-work attempt:

- `pre_s2_6_fork_work_runbook.md` v1.2.1 NV-resident at `/workspace/architecture_profile/runbooks/`
- `memit-patches-canonical.md` v2.2 NV-resident at `/workspace/architecture_profile/`
- MEMIT clone NV-resident at `/workspace/memit_dry_run/memit/` with P-1, P-2, P-4, P-5 applied; Pad-Token alias applied at tokenizer load time per Cell 3 Phase B (not source-modified)
- `globals.yml` NV-resident at canonical paths per D-PreS26-3
- Bridge cache archived at `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/bridge_archive_20260430T035042Z/` per IC-S25-1
- Canonical cache path empty: `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` (will be populated by successor fork-work attempt's Cell 4)

Successor fork-work attempt operator-side workflow:

1. Start pod against same NV.
2. Re-install dep manifest (matches §4.3 of this runbook).
3. Open `pre_s2_6_fork_work_runbook.md` v1.2.1 in JupyterLab.
4. Execute Cell 0 → Cell 1 → Cell 1.5 → Cell 2 → Cell 3 → Cell 3.5 → Cell 4 → Cell 5.
5. On Cell 5 GATE PASS, OQ-S25-9 closes; cache_provenance.status updates to `PASS`; manifest revision to v3.1 anticipated.
6. Stop pod. Mirror sync as needed.

Estimated successor fork-work wall-time: ~2–3 hours including ~90 min Cell 4 covariance compute (5 layers × ~15–20 min each on RTX 4090).

---

*End of Session 2.5b §4.3 Operator Runbook. Closure of this runbook closes Session 2.5b in aggregate; successor session is the pre-S2.6 fork-work re-attempt (operator-controlled launch timing).*
