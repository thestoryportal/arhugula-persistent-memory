# Session 2.3 — Partial Summary Block (At Pause)

## Bottom Line

Block 2 closed with HC-2 PASS verdict on RunPod RTX 4090 in US-NC-1. Block 3 (persistent state architecture) is pending. Session paused for operator sleep break with GPU pod terminated and NV preserved with all artifacts. Resume picks up at Block 3 Step 3.1 (directory layout commit) on a fresh pod whose first NV mount also satisfies the deferred Step 2.5d (across-teardown NV persistence test, OQ-S23-12).

## HC-2 Verdict — Locked

```
{
  "smoke_test": "MEMIT-COMPAT-PROTO-1 single-fact rehearsal (RunPod RTX 4090)",
  "completed_at": "2026-04-26T10:24:43.491958+00:00",
  "venue": "RunPod RTX 4090 24 GB Secure Cloud",
  "verdict": "PASS",
  "hc_2_verdict": "PASS",
  "assertions": {
    "SF_1_top1_is_baseball": true,
    "SF_2_p_baseball_gt_p_basketball": true,
    "SF_3_unmount_restores_basketball": true
  },
  "probabilities": {
    "P_basketball_pre":         0.8697880506515503,
    "P_baseball_pre":           0.021605264395475388,
    "P_baseball_post":          0.9831444025039673,
    "P_basketball_post":        0.00034027741639874876,
    "P_basketball_postunmount": 0.8697880506515503,
    "P_baseball_postunmount":   0.021605264395475388
  },
  "drift_metrics": {
    "drift_p_baseball_post":                       0.0012812232142640342,
    "drift_p_basketball_post":                     0.47979768064038686,
    "drift_p_basketball_postunmount_intrapod":     0.0,
    "drift_p_basketball_postunmount_crossenv":     0.0004652241521474766
  }
}
```

Verdict file persisted at `/workspace/memit_dry_run/runpod_dry_run_verdict.json` (2,655 bytes; mtime 2026-04-26 10:24 UTC).

## Block 2 Execution Record

### Step 2.1 — Account provisioning (CLOSED)

| Item | State |
|---|---|
| Account verification | Cleared |
| Payment method | Confirmed |
| Account flags | None |
| $50 billing alert | Configured |
| $150 / $300 alerts | Deferred (OQ-S23-1; manual cost monitoring) |

### Step 2.2 — NV provisioning (CLOSED)

| Item | Value |
|---|---|
| NV name | `large_amethyst_wolverine` |
| NV size | 100 GB |
| NV region | US-NC-1 |
| NV mount path | `/workspace` |
| Filesystem | MooseFS (`mfs#us-nc-1.runpod.net:9421`) |

Region selection rationale: US-NC-1 was selected by the operator at deploy time when the original priority list (US-OR-1, US-KS-2, US-TX-3) did not match the current RunPod regional inventory. US-OR-1 is no longer a region. Region priority list now stale — see OQ-S23-2-region (region inventory drift).

### Step 2.3 — Image digest pinning (CLOSED)

```
runpod/pytorch@sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5
Tag (informational): 2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
Runtime PyTorch:     2.4.1+cu124  ← differs from tag-implied 2.4.0
Runtime Python:      3.11.10
Runtime CUDA (torch): 12.4
Runtime CUDA (driver): 12.8 (driver 570.195.03)
Runtime cuDNN:       90100 (9.1.0)
GPU compute:         sm_89
```

OQ-S23-2: RunPod ships patch-level updates without re-tagging. Manifest must record runtime-observed versions, not tag-implied versions.

### Step 2.4 — HC-2 dry-run (PASS)

10-cell canonical notebook executed against GPT-J 6B FP16 single-fact edit (`Michael Jordan plays the sport of` → ` baseball`). Wall time ~3-4 min for Cell 6 MEMIT edit (vs ~7-8 min on Kaggle T4 with CPU solve — RTX 4090 GPU FP64 solve is ~50% faster).

Notable cell-level events during execution:

| Cell | Outcome |
|---|---|
| 1 (env fingerprint) | PASS |
| 2 (joint 4.x stack install) | Initial PASS (5 packages installed; `datasets` import failed) |
| 2b (re-import correction) | PASS |
| 2c (datasets install) | PASS — added after Cell 6 surfaced `datasets` as transitive import-time dep |
| 2d (matplotlib/scipy/sklearn/pandas install) | Partial — sklearn verification raised on pandas C extension mismatch |
| 2e (pandas force-reinstall) | Did not resolve — C extension dlopen handle cached in interpreter |
| Kernel restart | EXECUTED — required to evict cached C extensions (OQ-S23-8) |
| Cell 2-restart-verify (post-restart) | PASS |
| Cell 3-rebind (post-restart) | PASS — replaces Cell 3 to avoid `shutil.rmtree` destroying patches |
| 3 (MEMIT clone, original) | PASS |
| 4 (model load) | PASS, 12.10 GB GPU memory |
| 5 (pre-edit) | PASS, top-1 = `' basketball'` |
| 5b (pad_token) | PASS |
| 5e (P-1+P-2 patch) | PASS, +202 chars |
| 6 (MEMIT edit) | PASS after Cells 2c/2d/2e/restart sequence; `nan_check=False`, `Delta norm 67.9999` |
| 7 (post-edit) | SF-1, SF-2 PASS |
| 8 (overlay save + copy_() unmount) | PASS, all 6 layers `match=True` |
| 9 (post-unmount) | SF-3 PASS, top-1 = `' basketball'` restored bit-identically |
| 10 (verdict, OQ-S23-3 amended) | HC-2 PASS |

### Step 2.5a — Final artifact audit (CLOSED)

```
Artifact                                                  Size      State
/workspace/memit_dry_run/runpod_dry_run.ipynb            47,027 B   present
/workspace/memit_dry_run/runpod_dry_run_verdict.json      2,655 B   present
/workspace/memit_dry_run/smoke_test_overlay/edited.pt   805 MB     present
/workspace/memit_dry_run/smoke_test_overlay/original.pt 805 MB     present
/workspace/memit_dry_run/memit/                         ~25 MB     present
/workspace/memit_dry_run/memit/util/nethook.py          15,708 B   P-1+P-2 patched
/workspace/memit_dry_run/memit/data/stats/                6.1 GB   present (covariance cache)
/workspace/memit_dry_run/.ipynb_checkpoints/              small    present

Total memit_dry_run/ size:                                7.6 GB
NV utilization:                                           7.6 GB / 100 GB (8%)
```

### Step 2.5b — GPU pod termination (CLOSED)

`aesthetic_emerald_wallaby` terminated. NV `large_amethyst_wolverine` detached and intact. Termination occurred ahead of US-NC-1 capacity unavailability discovery.

### Step 2.5c — Cheap pod spin-up (NOT EXECUTED)

US-NC-1 reported all GPU instances unavailable at deploy attempt. RTX 4090 and RTX 5090 both showed "Out of Stock". Community Cloud RTX 5000 was offered and rejected per Session 2.1 venue lock (Secure Cloud only; OQ-S23-13 documents the procurement decision question for forward routing).

### Step 2.5d — NV persistence test (DEFERRED)

OQ-S23-12: Across-teardown NV persistence test deferred from Session 2.3 due to US-NC-1 GPU capacity unavailability. Verification opportunity is the resume pod mount.

## Decisions Made

1. **Path C (Block 3 on existing GPU pod)** approved when US-NC-1 cheap-pod tier capacity unavailable. Subsequently rendered moot by GPU pod termination.
2. **Community Cloud RTX 5000 rejected.** Maintains Session 2.1 venue lock on Secure Cloud. OQ-S23-13 routes the broader procurement question to Session 2.5 Stage 1 prep.
3. **OQ-S23-3 spec amendment.** Cell 10 acceptance band for `P_basketball_postunmount` reformulated from cross-environment 1e-6 to intra-pod 1e-4. Empirical drift was 0.0 (bit-identical), confirming `.vindex` overlay isolation as a strict bit-identity property, not noise-floor.
4. **Symlink (not move) for covariance cache canonical layout.** Selected for Step 3.1 to preserve MEMIT's hardcoded relative path resolution while satisfying the canonical `/workspace/covariance_caches/` layout queryability.
5. **Pre-pause termination of GPU pod.** Cost during sleep ($0.69/hr × 7 hr ≈ $4.83) exceeded value of resume readiness (3 min new-pod deploy). NV storage cost during pause: ~$0.07.
6. **`datasets==4.8.3` Kaggle parity pin** for cross-environment manifest reproducibility.

## Constraints Established

1. **Import-time dependency closure must be exhaustive, not incremental.** Discovery-by-failure incompatible with C extension caching (OQ-S23-4 / OQ-S23-8 refinement).
2. **C extension version mismatches require kernel restart**, not `sys.modules` purge alone. Pip's `--force-reinstall` replaces files on disk but does not invalidate `dlopen()` handles cached in the running interpreter.
3. **Cell 3 idempotence violation logged**: `shutil.rmtree("memit")` destroys patches applied by Cell 5e. Stage 1+ runbooks must guard or document this.
4. **`.vindex` overlay isolation is bit-identical**, not noise-floor. The Cell 8 `copy_()` unmount produces mathematically perfect parameter restoration. Stage 1+ spec invariant elevation candidate (OQ-S23-11).
5. **RunPod image patch-level updates without re-tagging.** Image digest is the only reliable reproducibility anchor; tag is informational (OQ-S23-2).
6. **Region priority list stale.** US-OR-1 absent from current RunPod region inventory. US-KS-2, US-IL-1, US-NC-1, US-TX-3 are the available US options; US-NC-1 is the operative selection (NV-pinned).

## Open Questions Deferred

See `oq-s23-backlog.md` for full entries. Summary:

| ID | Class | Closes at |
|---|---|---|
| OQ-S23-1 | Procurement | Stage 1 prep |
| OQ-S23-2 | Manifest discipline | Stage 1 runbook |
| OQ-S23-3 | Spec amendment | CLOSED (Cell 10 amendment applied) |
| OQ-S23-4 | Runbook authorship | Stage 1 runbook |
| OQ-S23-5 | Cache strategy | Stage 1 prep |
| OQ-S23-6 | Spec hygiene | Stage 1 runbook |
| OQ-S23-7 | Idempotence | Stage 1 runbook |
| OQ-S23-8 | Failure mode taxonomy | Stage 1 runbook |
| OQ-S23-9 | Diagnostic logging variance | Stage 1 runbook |
| OQ-S23-10 | Forward dependency | MEMIT fork (OQ-S22-17) |
| OQ-S23-11 | Spec invariant elevation | Workstream 3 |
| OQ-S23-12 | Test deferred | Resume pod mount |
| OQ-S23-13 | Procurement | Session 2.5 Stage 1 prep |

## Interface Contracts Defined

### IC-S23-1 — Reproducibility Manifest Block 2 Fields

```
runpod_dry_run = {
  "pod_image_digest":         "sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5",
  "completed_at":             "2026-04-26T10:24:43.491958+00:00",
  "edit_success_metric":      "PASS (HC-2 SF-1, SF-2, SF-3 + amended drift bands)",
  "drift_from_kaggle": {
    "p_baseball_post":                       0.0012812232142640342,
    "p_basketball_post":                     0.47979768064038686,
    "p_basketball_postunmount_intrapod":     0.0,
    "p_basketball_postunmount_crossenv":     0.0004652241521474766
  },
  "venue":                    "RunPod Secure Cloud",
  "region":                   "US-NC-1",
  "gpu":                      "NVIDIA GeForce RTX 4090",
  "gpu_compute":              "sm_89"
}
```

### IC-S23-2 — Reproducibility Manifest Persistent State Fields

```
persistent_state = {
  "network_volume_id":               "<RunPod NV ID — to be captured at resume>",
  "network_volume_name":             "large_amethyst_wolverine",
  "network_volume_region":           "US-NC-1",
  "network_volume_size_gb":          100,
  "directory_layout_committed":      <true on Step 3.1 closure>,
  "across_teardown_test_completed":  <true on Step 2.5d completion at resume>
}
```

### IC-S23-3 — Reproducibility Manifest rsync Fields

```
rsync_target = {
  "local_path":  "<operator MBP path — to be defined at Step 3.2>",
  "cadence":     "weekly",
  "ssh_method":  "<RunPod SSH-over-Internet | other — to be defined at Step 3.2>"
}
```

### IC-S23-4 — Cell 10 Amendment Provenance

```
spec_amendment_record = {
  "id":          "OQ-S23-3",
  "applied_in":  "Session 2.3, Cell 10 dry-run notebook",
  "change":      "drift_p_basketball_postunmount: cross-env 1e-6 → intra-pod 1e-4",
  "rationale":   "Cross-env band tested architecture-pair FP16 dispatch differences (sm_75 vs sm_89), not overlay isolation. Intra-pod band tests the load-bearing .vindex framework property. Empirical intra-pod drift was 0.0 (bit-identical).",
  "carries_to":  "Stage 1 SECT runbook acceptance band specifications"
}
```

## Carry-Forward to Resume Turn

The next session turn must:

1. Confirm pod state (terminated; NV detached and intact).
2. Verify US-NC-1 RTX 4090 capacity before deploy.
3. Deploy with image digest pin per IC-S23-1.
4. Execute Step 2.5d on first NV mount (closes OQ-S23-12).
5. Execute Block 3 Steps 3.1, 3.2, 3.3.
6. Emit Session Summary Block (full, not partial).
7. Terminate resume pod.

Detailed sequence: `block-3-resume-execution-plan.md`.

## Next Session Candidates

After Session 2.3 closure:

- **Session 2.4** — CFB v1 corpus authorship + probe-set v1 authorship (Workstream 1; blocked on Session 2.3 closure)
- **Session 2.5** — Stage 1 SECT execution prep + LLaMA 3.1 8B target model commitment (blocked on Session 2.4; some prep is path-independent per IC-WS1-1)
