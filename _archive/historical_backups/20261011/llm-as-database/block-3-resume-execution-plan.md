# Block 3 Resume — Execution Plan

## 1. Scope

This document specifies the resume sequence for Session 2.3 from pause state. It covers Step 2.5c (resume pod deploy), Step 2.5d (NV persistence test, executes naturally on first mount), Step 3.1 (NV directory layout commit), Step 3.2 (rsync configuration), Step 3.3 (manifest finalization), and session closure.

## 2. Pre-Deploy State Verification

### 2.1 RunPod console verification (operator action, ~1 min)

```
RunPod Console
    └── Storage → Network Volumes
        └── large_amethyst_wolverine
            └── Verify: 100 GB, US-NC-1, attached pods = 0
            └── Verify: Status = Active (not "Marked for deletion")
```

If NV listing shows `attached pods > 0`, a stale pod attachment exists. Halt and investigate via RunPod console pod listing.

### 2.2 Capacity verification (operator action, ~30 sec)

```
RunPod Console
    └── Pods → Deploy
        └── Filter: GPU Type = RTX 4090, Region = US-NC-1, Cloud Type = Secure Cloud
        └── Read availability indicator
```

Acceptable outcomes:

| Outcome | Action |
|---|---|
| 2.2.1 — RTX 4090 available in US-NC-1 (any availability) | Proceed to Section 3 |
| 2.2.2 — RTX 4090 unavailable; RTX 5090 available in US-NC-1 | Proceed to Section 3 with RTX 5090 substitution |
| 2.2.3 — No GPUs available in US-NC-1 | Wait + retry every 5-10 min; reject Community Cloud per OQ-S23-13 |

## 3. Step 2.5c — Resume Pod Deploy

### 3.1 Pod specifications

| Setting | Value | Source |
|---|---|---|
| GPU type | RTX 4090 (preferred); RTX 5090 (fallback) | Section 2.2 outcome |
| GPU count | 1 | Single-GPU envelope |
| Region | US-NC-1 | NV-pinned (non-negotiable) |
| Cloud type | Secure Cloud | Session 2.1 lock |
| Pod type | On-Demand | Session 2.1 lock |
| Container image | `runpod/pytorch@sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5` | IC-S23-1 |
| Container disk | 10 GB minimum | No model loads required |
| Network Volume | `large_amethyst_wolverine` mounted at `/workspace` | Block 2 work product |
| Pod name | Operator preference (e.g., `block3_resume`) | — |

### 3.2 Deploy verification (operator action, ~1 min)

After clicking Deploy On-Demand, wait for pod state `running`. In the pod's web terminal:

```bash
hostname
date
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
```

Expected: hostname differs from `71f56d183e06`; date is post-pause; GPU is RTX 4090 (or RTX 5090 fallback); memory.total ~24576 MiB (RTX 4090) or ~32768 MiB (RTX 5090).

### 3.3 Deploy reportable

```
Resume pod deploy:
  Pod ID:                  pod-XXXXXXXXX
  Pod name:                <selected>
  GPU type:                <RTX 4090 | RTX 5090>
  Hourly rate:             $<X.XX>/hr
  Region:                  US-NC-1
  Hostname:                <new>
  Pod state:               running
```

## 4. Step 2.5d — NV Persistence Test (Closes OQ-S23-12)

### 4.1 Test commands (operator action, ~30 sec)

```bash
# 4.1.1 — Verify NV mount
df -h /workspace

# 4.1.2 — Verify Block 2 work product survived NV detach/attach cycle
ls -la /workspace/memit_dry_run/

# 4.1.3 — Verify verdict JSON content
head -10 /workspace/memit_dry_run/runpod_dry_run_verdict.json
md5sum /workspace/memit_dry_run/runpod_dry_run_verdict.json

# 4.1.4 — Verify covariance cache survived
du -sh /workspace/memit_dry_run/memit/data/stats/

# 4.1.5 — Verify patched nethook.py survived
grep -c "with_kwargs=True" /workspace/memit_dry_run/memit/util/nethook.py

# 4.1.6 — Verify overlay tensors survived
ls -la /workspace/memit_dry_run/smoke_test_overlay/
```

### 4.2 Expected anchors

| Verification | Pre-pause value | Post-mount expectation |
|---|---|---|
| `df -h /workspace` | `mfs#us-nc-1.runpod.net:9421 1.2P` | Same MFS endpoint |
| `memit_dry_run/` entry count | 5 (excluding `.` and `..`) | 5 |
| `runpod_dry_run.ipynb` size | 47,027 B | 47,027 B |
| `runpod_dry_run_verdict.json` size | 2,655 B | 2,655 B |
| `verdict.json` head -10 | Begins `{ "smoke_test": ...` | Bit-identical |
| `memit/data/stats/` size | 6.1 GB | 6.1 GB |
| `with_kwargs=True` count in nethook | 1 | 1 |
| `smoke_test_overlay/edited.pt` size | 805,308,606 B | 805,308,606 B |
| `smoke_test_overlay/original.pt` size | 805,309,074 B | 805,309,074 B |

### 4.3 Halt rules

| Symptom | Action |
|---|---|
| 4.3.1 — `df -h /workspace` returns "not mounted" or different filesystem | Halt; verify NV attachment in RunPod console |
| 4.3.2 — Any artifact missing or size mismatch | Halt; capture forensic evidence; escalate to RunPod NV-detach/attach SLA inquiry |
| 4.3.3 — `with_kwargs=True` count != 1 in nethook.py | Patch loss; halt; OQ-S23-12 closes as FAIL |
| 4.3.4 — Verdict JSON content corrupted | Halt; HC-2 verdict provenance broken; consider re-running Cells 1-10 |

### 4.4 OQ-S23-12 closure on PASS

If all anchors match, OQ-S23-12 closes as PASS. The result feeds the manifest field `persistent_state.across_teardown_test_completed = true`. Empirical confirmation strengthens the IC-S23-2 contract.

### 4.5 Step 2.5d reportable

```
Step 2.5d NV persistence test:
  df -h /workspace:                 <output>
  memit_dry_run/ entry count:       <N>
  runpod_dry_run.ipynb:             <bytes>
  runpod_dry_run_verdict.json:      <bytes>
  verdict.json md5:                 <hash>
  covariance cache size:            <X.X GB>
  nethook with_kwargs count:        <N>
  edited.pt size:                   <bytes>
  original.pt size:                 <bytes>
  OQ-S23-12 closure verdict:        <PASS | FAIL>
```

## 5. Step 3.1 — NV Directory Layout Commit

### 5.1 Target structure

```
/workspace/
├── architecture_profile/             # PF-1..PF-6 outputs at Stage 1
├── vindex_overlays/                  # MEMIT edit overlays per stage
├── cfb_baseline/                     # CFB v1 corpus + pre-edit baseline
├── covariance_caches/                # PF-5 covariance matrices (canonical)
│   └── EleutherAI_gpt-j-6B/          # → symlinked to memit_dry_run/memit/data/stats/EleutherAI_gpt-j-6B/
├── drift_sweep_results/              # Stage 2 outputs
├── epsilon_calibration/              # Stage 3a outputs
├── compaction_probe_calibration/     # Stage 3b outputs
├── judge_calibration/                # Stage 3c outputs
├── session_logs/                     # per-session execution logs
│   └── session_2_3_block_2_verdict.json
├── reproducibility_manifest.json     # the pinned-version record (Step 3.3)
└── memit_dry_run/                    # Block 2 work product (preserve)
    ├── memit/
    ├── runpod_dry_run.ipynb
    ├── runpod_dry_run_verdict.json
    ├── smoke_test_overlay/
    └── .ipynb_checkpoints/
```

### 5.2 Migration policy

Covariance cache migration: **symlink, not move**. MEMIT's hardcoded relative path resolution depends on `memit/data/stats/...`; canonical layout requires `/workspace/covariance_caches/`. Symlink satisfies both.

### 5.3 Step 3.1 commands (operator action, ~2 min)

```bash
# 5.3.1 — Create canonical layout directories
cd /workspace
mkdir -p architecture_profile \
         vindex_overlays \
         cfb_baseline \
         covariance_caches \
         drift_sweep_results \
         epsilon_calibration \
         compaction_probe_calibration \
         judge_calibration \
         session_logs

# 5.3.2 — Symlink covariance cache to canonical path
ln -s /workspace/memit_dry_run/memit/data/stats/EleutherAI_gpt-j-6B \
      /workspace/covariance_caches/EleutherAI_gpt-j-6B

# 5.3.3 — Initialize session_logs/ with the Block 2 verdict reference
cp /workspace/memit_dry_run/runpod_dry_run_verdict.json \
   /workspace/session_logs/session_2_3_block_2_verdict.json

# 5.3.4 — Verify layout
ls -la /workspace/
ls -la /workspace/covariance_caches/
ls -la /workspace/session_logs/

# 5.3.5 — Confirm symlink resolves
du -sh /workspace/covariance_caches/EleutherAI_gpt-j-6B/
ls /workspace/covariance_caches/EleutherAI_gpt-j-6B/ | wc -l
```

### 5.4 Expected output anchors

| Command | Expected |
|---|---|
| 5.3.4 first `ls` | 11 entries: 9 new directories + `memit_dry_run/` + (later, after 3.3) `reproducibility_manifest.json` |
| 5.3.4 second `ls` | One symlink: `EleutherAI_gpt-j-6B -> /workspace/memit_dry_run/...` |
| 5.3.4 third `ls` | `session_2_3_block_2_verdict.json` (2,655 bytes) |
| 5.3.5 `du -sh` | 6.1 GB (resolves through symlink) |
| 5.3.5 `wc -l` | 6 (one .npz per layer 3-8) |

### 5.5 Step 3.1 reportable

```
Step 3.1 directory layout:
  /workspace/ root listing (paste full ls -la)
  /workspace/covariance_caches/ listing
  /workspace/session_logs/ listing
  Symlink resolution (du -sh):                      <X.X GB>
  Layer-specific .npz files visible through symlink: <count>
  Block 2 verdict copied to session_logs:           <yes | no>
```

## 6. Step 3.2 — rsync Configuration

### 6.1 Sub-decisions required from operator

| Sub-decision | Required value | Notes |
|---|---|---|
| 6.1.1 — Local mirror target path | e.g., `/Users/<operator>/llm-database-poc-mirror/` | Operator selects |
| 6.1.2 — SSH key for RunPod pod | Existing SSH key in RunPod console, OR generate new | RunPod has SSH-over-Internet feature |
| 6.1.3 — Disk headroom on MBP | At minimum 10 GB | Block 2 NV state is 7.6 GB; Stage 1 will grow |

### 6.2 RunPod SSH access setup (operator action, one-time)

```
RunPod Console
    └── Settings → SSH Keys
        └── Add public key
            └── Paste contents of ~/.ssh/id_ed25519.pub (or id_rsa.pub) from MBP
```

Pod-level SSH endpoint visible at: Pods → resume_pod → Connect → SSH dropdown. Format:

```
ssh root@<pod-ip> -p <port> -i ~/.ssh/id_ed25519
```

### 6.3 rsync command pattern

Initial full sync (~7.6 GB; ~5-15 min over residential connection):

```bash
# On operator's MBP
mkdir -p /Users/<operator>/llm-database-poc-mirror/

rsync -avz --progress \
    -e "ssh -p <runpod-pod-port> -i ~/.ssh/id_ed25519" \
    root@<runpod-pod-ip>:/workspace/ \
    /Users/<operator>/llm-database-poc-mirror/
```

Subsequent incremental sync (weekly cadence):

```bash
rsync -avz --delete --progress \
    -e "ssh -p <runpod-pod-port> -i ~/.ssh/id_ed25519" \
    root@<runpod-pod-ip>:/workspace/ \
    /Users/<operator>/llm-database-poc-mirror/
```

The `--delete` flag in incremental mode propagates NV-side deletions; this is the desired weekly-mirror behavior. Initial sync omits `--delete` to be safe.

### 6.4 Important rsync semantics

| Behavior | Detail |
|---|---|
| Source of truth | RunPod NV during POC. Local MBP mirror is backup, not authoritative |
| `--delete` direction | Files deleted on NV are removed from local mirror; never reverse |
| Symlinks | `-a` preserves symlinks as symlinks; rsync does not chase the canonical-path symlink to the covariance cache |
| Bandwidth | RunPod allows free egress; throttling depends on operator's residential ISP |
| SSH port | Varies per pod; captured in deploy step |

### 6.5 Initial sync execution (operator action, ~5-15 min)

Operator runs the initial rsync command from their MBP terminal. Wall time depends on residential bandwidth (300 Mbps ≈ 4 min for 7.6 GB).

### 6.6 Step 3.2 reportable

```
Step 3.2 rsync configuration:
  Local mirror path:                    <path on MBP>
  SSH key used:                         <key fingerprint, e.g., ed25519:XXXXX>
  RunPod pod SSH endpoint:              <ip:port>
  Initial sync wall time:               <approx min>
  Local mirror size after initial sync: <X.X GB>
  Sync cadence:                         weekly
  rsync command pattern stored at:      <e.g., ~/scripts/rsync-runpod-mirror.sh>
```

## 7. Step 3.3 — Reproducibility Manifest Finalization

### 7.1 Source manifest

The pre-existing `architecture-profile-seed.json` at the project root contains Block 1 (Kaggle smoke test) values. Block 2 fields (`runpod_dry_run`), persistent state fields, and rsync target fields are populated in this step.

### 7.2 Field population specification

```python
manifest_updates = {
    "runpod_dry_run": {
        "pod_image_digest": "sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5",
        "pod_image_tag":    "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04",
        "completed_at":     "2026-04-26T10:24:43.491958+00:00",
        "venue":            "RunPod Secure Cloud",
        "region":           "US-NC-1",
        "gpu":              "NVIDIA GeForce RTX 4090",
        "gpu_compute":      "sm_89",
        "gpu_memory_gb":    24,
        "edit_success_metric": "PASS (HC-2 SF-1, SF-2, SF-3 + amended drift bands)",
        "drift_from_kaggle": {
            "p_baseball_post":                       0.0012812232142640342,
            "p_basketball_post":                     0.47979768064038686,
            "p_basketball_postunmount_intrapod":     0.0,
            "p_basketball_postunmount_crossenv":     0.0004652241521474766
        },
        "pinned_versions_observed": {
            "python":           "3.11.10",
            "torch":            "2.4.1+cu124",
            "cuda_torch":       "12.4",
            "cuda_driver":      "12.8",
            "driver_version":   "570.195.03",
            "cudnn":            "90100",
            "transformers":     "4.45.2",
            "accelerate":       "0.34.2",
            "huggingface_hub":  "0.25.2",
            "tokenizers":       "0.20.3",
            "safetensors":      "0.4.5",
            "datasets":         "4.8.3",
            "matplotlib":       "3.9.2",
            "scipy":            "1.14.1",
            "pandas":           "2.2.3",
            "sklearn":          "1.5.2",
            "memit_repo_sha":   "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b",
            "gpt_j_revision":   "float16",
            "gpt_j_revision_sha": "b71ae8bc86cac13154e03e92b5855203086b722e"
        },
        "spec_amendments_applied": [
            {
                "id":          "OQ-S23-3",
                "applied_in":  "Cell 10 dry-run notebook",
                "change":      "drift_p_basketball_postunmount band: cross-env 1e-6 → intra-pod 1e-4",
                "rationale":   "Cross-env band tested architecture-pair FP16 dispatch differences (sm_75 vs sm_89), not overlay isolation. Intra-pod band tests the load-bearing .vindex framework property."
            }
        ]
    },

    "persistent_state": {
        "network_volume_id":          "<TO BE CAPTURED FROM RUNPOD CONSOLE>",
        "network_volume_name":        "large_amethyst_wolverine",
        "network_volume_region":      "US-NC-1",
        "network_volume_size_gb":     100,
        "network_volume_used_gb_at_block2_close": 7.6,
        "directory_layout_committed": True,
        "across_teardown_test_completed": True,
        "across_teardown_test_verdict":   "<PASS | FAIL from Step 2.5d>"
    },

    "rsync_target": {
        "local_path":  "<from Step 3.2.1>",
        "cadence":     "weekly",
        "ssh_method":  "RunPod SSH-over-Internet",
        "initial_sync_completed_at": "<ISO timestamp from Step 3.2.5>",
        "initial_sync_size_gb":      7.6,
        "command_pattern_stored_at": "<e.g., ~/scripts/rsync-runpod-mirror.sh>"
    },

    "billing_alerts": {
        "alert_50":  "configured",
        "alert_150": "deferred — OQ-S23-1",
        "alert_300": "deferred — OQ-S23-1",
        "manual_monitoring": "operator daily RunPod console check"
    }
}
```

The NV ID (a RunPod-internal UUID-like value) must be captured from the RunPod console's Storage → Network Volumes → `large_amethyst_wolverine` → details panel. Format: `nvol-XXXXXXXXX`.

### 7.3 Step 3.3 commands

```bash
# 7.3.1 — Locate the seed manifest in project knowledge
# (The manifest seed is in the project KB as architecture-profile-seed.json)
# Operator pulls a copy onto the pod for editing, OR edits locally and uploads.

# Option A: edit on pod
cat > /workspace/reproducibility_manifest.json <<'EOF'
{
  "$schema": "...",
  "block_1_kaggle": { ... },
  "runpod_dry_run": { ... per Section 7.2 ... },
  "persistent_state": { ... per Section 7.2 ... },
  "rsync_target": { ... per Section 7.2 ... },
  "billing_alerts": { ... per Section 7.2 ... }
}
EOF

# 7.3.2 — Validate JSON
python -c "import json; json.load(open('/workspace/reproducibility_manifest.json'))" \
  && echo "JSON valid"

# 7.3.3 — Verify file persisted on NV
ls -la /workspace/reproducibility_manifest.json
md5sum /workspace/reproducibility_manifest.json
```

### 7.4 Manifest assembly approach

Two viable paths:

| Path | Mechanism | Trade-off |
|---|---|---|
| 7.4.1 — Agent assembles manifest, operator pastes | Agent generates final JSON in chat output; operator pastes via heredoc | One-shot; faster |
| 7.4.2 — Operator writes Python script that merges seed + Block 2/3 fields | Script reads `architecture-profile-seed.json`, merges per Section 7.2, writes output | Reusable; auditable |

**Selection: 7.4.1** for Session 2.3. The reproducibility manifest is a one-shot artifact at this session boundary; reusability is not a current concern. Stage 1+ may benefit from path 7.4.2.

### 7.5 Step 3.3 reportable

```
Step 3.3 manifest finalization:
  Manifest file path:                   /workspace/reproducibility_manifest.json
  File size:                            <bytes>
  JSON validation:                      <valid | invalid>
  md5sum:                               <hash>
  NV ID captured:                       <nvol-XXXXXXXXX>
  Across-teardown test verdict:         <PASS | FAIL>
```

## 8. Session Summary Block Emission

After Step 3.3 closes, the agent emits the full Session Summary Block per the standard format defined in the Session 2.3 prompt. The block consolidates:

```
## Session Summary Block

### Decisions made
- [13+ decisions including HC-2 PASS, OQ-S23-3 amendment, Path C, Community
  Cloud rejection, symlink-not-move covariance migration, etc.]

### Constraints established
- [Import-time dep closure exhaustive; C extension restart class; Cell 3
  idempotence; .vindex bit-identical; image patch-level updates; region
  inventory drift]

### Open questions deferred
- [OQ-S23-1 through OQ-S23-13, with closure routing]

### Interface contracts defined
- [IC-S23-1, IC-S23-2, IC-S23-3, IC-S23-4]

### Next session candidates
- [Session 2.4 corpus authorship]
- [Session 2.5 Stage 1 prep]
```

This block becomes the input to Session 2.4. Persisted at `/workspace/session_logs/session_2_3_summary_block.md` and exported back to project KB.

## 9. Pod Termination

After Session Summary Block emission and persistence to NV:

```
RunPod Console
    └── Pods → resume_pod → ⋮ → Terminate → Confirm
```

NV `large_amethyst_wolverine` continues accruing $0.01/hr storage. Block 2 + 3 work product persists for Sessions 2.4, 2.5, and Stage 1.

## 10. Total Session 2.3 Resume Wall Time

| Phase | Estimate |
|---|---|
| Capacity check + deploy | ~3 min |
| Step 2.5d NV persistence test | ~2 min |
| Step 3.1 directory layout | ~2 min |
| Step 3.2 rsync configuration | ~10-20 min (initial sync dominates) |
| Step 3.3 manifest finalization | ~5 min |
| Session Summary Block | ~5 min |
| Termination | ~1 min |
| **Total resume** | **~30-40 min** |

Cost projection: ~$0.40 (RTX 4090 at $0.69/hr × 0.5 hr).

## 11. Halt Conditions

Session 2.3 resume halts on any of:

| Condition | Class | Recovery |
|---|---|---|
| 11.1 — US-NC-1 capacity unavailable for > 60 min | Capacity | Pause longer; consider OQ-S23-13 escalation only with operator authorization |
| 11.2 — NV persistence test (Step 2.5d) FAIL | Data loss | Forensics; potential Block 2 re-run |
| 11.3 — Symlink creation fails (5.3.2) | Filesystem | Investigate; consider move-instead-of-symlink fallback |
| 11.4 — rsync SSH fails | Network | Retry with verbose flag; check RunPod SSH key registration |
| 11.5 — Manifest JSON validation fails | Spec | Halt; correct JSON; reattempt |

All halt conditions feed back to Session 2.3 resume as deferred items rather than failure-of-session. The HC-2 PASS verdict is independent of these and remains locked.
