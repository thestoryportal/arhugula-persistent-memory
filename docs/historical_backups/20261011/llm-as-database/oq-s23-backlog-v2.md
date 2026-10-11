# OQ-S23-* Backlog v2 — Session 2.3 Open Questions (Closed PASS)

## 1. Purpose

Comprehensive registry of all open questions logged during Session 2.3 with full context for forward routing. v2 supersedes v1: this version reflects the session's final state at 2026-04-28 close, including 5 closures and 6 new entries surfaced during Block 3 execution.

Format follows the framework's gap backlog convention.

## 2. Backlog Summary

| ID | Class | Status at session close | Closes at |
|---|---|---|---|
| OQ-S23-1 | Procurement | Deferred | Stage 1 prep (Session 2.5) |
| OQ-S23-2 | Manifest discipline | Deferred | Stage 1 runbook |
| OQ-S23-3 | Spec amendment | **CLOSED** (Cell 10 amendment applied) | n/a |
| OQ-S23-4 | Runbook authorship | Deferred (refined iteration 3) | Stage 1 runbook |
| OQ-S23-5 | Cache strategy | Deferred | Stage 1 prep (Session 2.5) |
| OQ-S23-6 | Spec hygiene | Deferred | Stage 1 runbook |
| OQ-S23-7 | Idempotence | Deferred | Stage 1 runbook |
| OQ-S23-8 | Failure mode taxonomy | Deferred | Stage 1 runbook |
| OQ-S23-9 | Diagnostic logging variance | Deferred | Stage 1 runbook |
| OQ-S23-10 | Forward dependency | Deferred | MEMIT fork (OQ-S22-17) |
| OQ-S23-11 | Spec invariant elevation | Deferred | Workstream 3 implementation |
| OQ-S23-12 | Test deferred | **CLOSED PASS** (NV persistence verified across 2 cycles) | n/a |
| OQ-S23-13 | Procurement | Deferred | Session 2.5 Stage 1 prep |
| OQ-S23-14 | Filesystem hygiene (NEW) | Deferred | Session 2.4 prep, low priority |
| OQ-S23-15 | Resource budget (NEW) | **CLOSED** (external SSD relieves constraint) | n/a |
| OQ-S23-16 | Procurement (NEW) | Deferred | Session 2.5 Stage 1 prep |
| OQ-S23-17 | Runbook authorship (NEW) | **CLOSED** (rsync installed via apt) | n/a |
| OQ-S23-18 | Runbook authorship (NEW) | **CLOSED** (skopeo installed via apt) | n/a |
| OQ-S23-19 | Tooling — terminal paste limit (NEW) | Deferred | Stage 1 runbook |

**Summary at session close:** 5 CLOSED, 14 DEFERRED, 19 total.

## 3. OQ-S23-1 — Billing Alert Granularity Beyond $50

### 3.1 Question

RunPod's billing alert configuration was completed for the $50 threshold but deferred for $150 and $300 by operator decision. Is per-threshold automated alerting required for Stage 1+ cost monitoring, or is daily manual RunPod console check sufficient?

### 3.2 Context

Session 2.1 specified three thresholds ($50, $150, $300) as escalating cost circuits during Block 2 (smoke test footprint), Stage 1 mid-point (3 facts × 3 runs), and POC monthly cap respectively. Operator deferred the $150 and $300 thresholds without specifying configuration of fallback monitoring.

### 3.3 Implication for Stage 1+

Stage 1 SECT execution projects ~$10 GPU + NV. Reaching $50 indicates Stage 1 underway; $150 indicates Stage 2 sweep underway or unexpected leak. Without automated alerts, the discovery of cost anomaly is delayed to operator's manual check cadence.

### 3.4 Forward routing

Stage 1 prep must define manual cost monitoring discipline (e.g., "operator checks RunPod console daily at session start"), or the operator authorizes $150 / $300 alert configuration during Stage 1 prep.

## 4. OQ-S23-2 — RunPod Image Patch-Level Updates Without Re-Tagging

### 4.1 Question

The image tag `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` resolved to runtime PyTorch 2.4.1+cu124, not 2.4.0. RunPod ships patch-level updates without re-tagging. How should manifest discipline accommodate this?

### 4.2 Context

Cell 1 environment fingerprint reported PyTorch 2.4.1; the digest `sha256:61a4aafb...` correctly identifies the actual byte content. Tag-vs-runtime drift was logged on first observation.

### 4.3 Empirical refinement (Session 2.3 resume verification)

Across 2 distinct pod deployments separated by 2 days, runtime fingerprint matched bit-exact (Python 3.11.10 / PyTorch 2.4.1+cu124 / CUDA 12.4 / cuDNN 90100 / sm_89). Combined with skopeo `Created: 2024-09-24` (~19 months stable), risk for *this specific tag* is empirically low. Discipline (digest pinning) remains correct as policy.

### 4.4 Implication for Stage 1+

Manifest reproducibility cannot rely on tag references alone. Image refreshes between sessions require re-extracting the digest from Docker Hub.

### 4.5 Forward routing

Stage 1 runbook must record runtime-observed versions in the manifest's `pinned_versions_observed` field, separate from tag-implied versions. Cell 1 expectations should be anchored to the digest. Image-refresh procedure must include digest re-extraction.

Refined constraint C4 (NEW): Stage 1+ runbook should pin against the explicit RunPod-version tag (e.g., `0.7.0-cu1241-torch241-ubuntu2204`) for human-readable correctness, not the legacy `2.4.0-py3.11-...` alias. Both tags resolve to the same digest, but the RunPod-version tag is self-describing of actual contents.

## 5. OQ-S23-3 — Cell 10 Cross-Env vs Intra-Pod Drift Band (CLOSED)

### 5.1 Question

The canonical Cell 10 acceptance band `drift_p_basketball_postunmount < 1e-6` tested cross-environment numerical equivalence (Kaggle vs RunPod), not the load-bearing `.vindex` overlay isolation property (intra-pod pre-edit vs post-unmount).

### 5.2 Resolution

Cell 10 amended in Session 2.3:

```python
# Removed:
# drift_unmount_basketball_crossenv < 1e-6   <- cross-env, tight band

# Added:
drift_unmount_basketball_intrapod = drift(P_BASKETBALL_POSTUNMOUNT, P_BASKETBALL_PRE)
HC_2_PASS = ... and drift_unmount_basketball_intrapod < 1e-4   # intra-pod, FP16 noise floor

# Cross-env retained as informational, not gating:
drift_unmount_basketball_crossenv = drift(P_BASKETBALL_POSTUNMOUNT,
                                          KAGGLE_BASELINE["P_basketball_postunmount"])
```

### 5.3 Empirical validation

| Metric | Measured |
|---|---|
| Intra-pod drift | 0.0 (bit-identical) |
| Cross-env drift | 4.65e-4 (sm_75 vs sm_89 dispatch) |

### 5.4 Status

CLOSED. Amendment is recorded in the IC-S23-4 contract and persists in the verdict JSON's `spec_amendment` field.

## 6. OQ-S23-4 — Import-Time Dependency Closure (Refined Iteration 3)

### 6.1 Question

`runpod/pytorch:2.4.0` does not pre-ship `datasets`, `matplotlib`, or compatible `pandas`. Three failure cycles occurred during Block 2: `datasets` (Cell 2c remediation), `matplotlib` (Cell 2d remediation), `pandas` C extension mismatch (Cell 2e + kernel restart).

### 6.2 Iteration 3 refinement

> The Stage 1+ runbook against `runpod/pytorch:2.4.0` (or any image with pre-installed scientific Python tooling at unknown versions) must perform **all dependency installation in a single cell at session start, before any import of MEMIT/rome/datasets/sklearn**. Sequence:
> 1. Pip install all required packages with `--force-reinstall --no-deps` for any package known to ship pre-installed at a different version.
> 2. **Restart the kernel** to evict cached C extensions.
> 3. Verify imports.
> 4. Proceed with MEMIT import chain.
>
> Discovery-by-failure is structurally incompatible with C extension caching and cannot be remediated without restart.

### 6.3 Empirical dependency manifest

See `block-2-3-runbook-deltas.md` Section 12 for the complete validated manifest.

### 6.4 Pattern alignment with system-binary class

The discovery-by-failure pattern recurred for system binaries during Block 3:
- skopeo (resume verification, Session 2.3)
- rsync (Phase 5 sync attempt, Session 2.3)

OQ-S23-17 and OQ-S23-18 capture the system-binary instances. The unified principle for Stage 1+ runbook: exhaustive install (Python pkgs + system binaries) at session start.

### 6.5 Forward routing

Stage 1 runbook authorship must adopt the install-then-restart pattern. The manifest from Section 12 of the deltas document is the validated baseline.

## 7. OQ-S23-5 — HuggingFace Cache Location

### 7.1 Question

Default HF cache at `/root/.cache/huggingface/hub/` is on container disk (20 GB ephemeral). Block 2's GPT-J 6B cache (~12 GB) was lost on pod termination. For Stage 1+ multi-pod cycles, should HF cache be redirected to NV?

### 7.2 Trade-off matrix

| Option | First-run | Subsequent run | NV space | Container disk | Configuration cost |
|---|---|---|---|---|---|
| Defer (container-disk cache) | ~5-8 min | ~5-8 min (cache miss after teardown) | 0 GB | ~13 GB | None |
| NV-backed cache | ~5-8 min | ~10 sec (cache hit) | ~13 GB GPT-J + ~16 GB LLaMA 3.1 8B = ~29 GB | None | `export HF_HOME=/workspace/hf_cache` at pod boot |

### 7.3 Forward routing

Stage 1 prep must decide. For 3 facts x 3 runs against LLaMA 3.1 8B, NV-backed cache saves ~5-8 min x 8 cache-miss runs = ~50 min wall time and ~$0.55 GPU cost; net positive vs ~$2/month NV storage cost.

## 8. OQ-S23-6 — Token-ID Expectation Source

### 8.1 Question

The Section 4.1.1 expected anchor table for Cell 5 (RunPod prompt) listed `target_new_id = 39780` for ` baseball`. Actual token id is 9283. The 39780 value was a transcription error from preliminary work, not from Kaggle verdict JSON.

### 8.2 Implication

Future runbook expectation tables must reference Kaggle verdict JSON values directly, not derived expectations.

### 8.3 Forward routing

Stage 1 runbook expectation tables must trace each anchor value to a verifiable source (Kaggle verdict JSON, MEMIT hyperparam JSON, or empirical pre-edit measurement). Derived expectations are unacceptable.

This OQ also applies to probe-set v1 authorship in Session 2.4: each probe expected output must be sourced from the actual model output, not a predicted value.

## 9. OQ-S23-7 — Cell 3 Idempotence Violation

### 9.1 Question

Cell 3's `shutil.rmtree("memit")` is intentional for clean re-clone but destroys patches applied by Cell 5e. Re-running Cell 3 silently invalidates Cell 5e's effect. The notebook spec assumes strict top-down execution.

### 9.2 Resolution candidates

```
A. Make Cell 3 conditional on "patch already applied" check
   (preserve clone if patches present)

B. Document Cell 3 -> Cell 5e re-run dependency explicitly

C. Adopt Cell 3-rebind pattern for post-first-execution
   (re-establishes sys.path without rmtree + clone)
```

### 9.3 Forward routing

Stage 1 runbook should adopt Option C as the canonical post-restart pattern. Cell 3 itself is canonical for first-execution; Cell 3-rebind handles post-restart and post-pause cases.

## 10. OQ-S23-8 — Failure Mode Taxonomy Refinement

### 10.1 Question

The session's recovery procedures must distinguish failure modes that require kernel restart from those that allow in-place retry. The C extension dlopen cache class was discovered empirically.

### 10.2 Taxonomy

| Failure mode | In-process retry safe? | Restart required? |
|---|---|---|
| `ModuleNotFoundError` (package absent) | Yes | No |
| `ImportError` (Python source missing) | Yes | No |
| Python source-only version mismatch | Yes (with sys.modules purge) | No |
| C extension version mismatch | **No** | **Yes** |
| Runtime `OutOfMemoryError` | No | Yes (torch allocator state corrupted) |
| NaN/Inf in mutated weights | No | Yes (model state corrupted) |
| Hung cell with no progress > 15 min | Conditional | Conditional |
| Suspected `sys.modules` corruption after monkey-patch | Conditional | Conditional |

### 10.3 Forward routing

Stage 1 runbook recovery procedures must classify failures by this taxonomy. The "in-place retry" policy used during early Block 2 was not always correct.

## 11. OQ-S23-9 — `Tying optimization objective to N` Reporting Variance

### 11.1 Question

Kaggle MEMIT log reported `Tying optimization objective to 8`. RunPod MEMIT log reported `Tying optimization objective to 27`. Both produced equivalent `Delta norm` (within 1e-5) and equivalent `v*` final loss/p_target (within Adam noise).

### 11.2 Diagnosis

Benign reporting difference, not a behavioral defect. The reported value reflects a transformers version-dependent path in MEMIT's `compute_z.py` (transformers 4.45 vs the era-of-MEMIT version). Both paths produce the same `v*` target.

### 11.3 Forward routing

Stage 1 runbook should capture which transformers version produces which reported tying layer. The diagnostic log line is informational; manifest correctness is established by `Delta norm` and per-layer `orig_norm` / `upd_norm` matching Kaggle baselines, not by this reporting line.

## 12. OQ-S23-10 — `past_key_values` Deprecation Forward Path

### 12.1 Question

transformers 4.45.2 emitted deprecation warning during MEMIT edit:

```
We detected that you are passing `past_key_values` as a tuple of tuples.
This is deprecated and will be removed in v4.47. Please convert your cache
or use an appropriate `Cache` class.
```

MEMIT's `compute_z.py` constructs past_key_values manually as nested tuples; transformers 4.47+ requires `Cache` objects.

### 12.2 Forward routing

When MEMIT is forked (Session 2.2 OQ-S22-17), update past_key_values construction to the `Cache` class API ahead of any future transformers upgrade beyond 4.46.

This is a forward-compatibility task, not currently blocking; current pin is transformers 4.45.2.

## 13. OQ-S23-11 — `.vindex` Overlay Isolation Spec Invariant Elevation

### 13.1 Question

The OQ-S23-3 amendment specified `drift_p_basketball_postunmount_intrapod < 1e-4` as the acceptance band. Empirical drift was 0.0 (bit-identical). Should the `.vindex` framework spec invariant be elevated from "approximately mountable/unmountable" to "exactly mountable/unmountable"?

### 13.2 Implication

| Current spec language | Refined spec language |
|---|---|
| "Cell 8 invariant: torch.allclose(post_unmount, pre_edit) with default tolerance" | "Cell 8 invariant: post_unmount.equal(pre_edit) — bit-identity at FP16 representation" |

The Universal Patch (Copy-Unmount, Session 2.2 OQ-S22-32) yields a mathematically perfect overlay round-trip. Both pre-edit and post-unmount probabilities equal `0.8697880506515503` to all 16 displayed digits.

### 13.3 Forward routing

Workstream 3 implementation planning. The spec invariant elevation impacts:
- `.vindex` test suite design (bit-identity assertion vs allclose)
- Stage 1+ acceptance bands (which can rely on bit-identity for overlay isolation)
- Framework documentation language (overlay isolation as a hard guarantee)

## 14. OQ-S23-12 — Across-Teardown NV Persistence Test (CLOSED PASS)

### 14.1 Question

Step 2.5d (canonical RunPod NV persistence test: tear down GPU pod -> spin up cheap pod -> verify NV state survives) was deferred from Session 2.3 due to US-NC-1 GPU capacity unavailability after GPU pod termination.

### 14.2 Resolution

Test executed naturally on Session 2.3 resume. Two complete across-teardown cycles passed:

| Cycle | Quiescence | Pod transition | Anchor count | Bit-identity |
|---|---|---|---|---|
| Cycle 1 (Phase 3) | ~9 hours | Block 2 pod (`71f56d183e06`) -> resume pod 1 (`fe48f0d87f5e`) | 10 | YES |
| Cycle 2 (Gate B) | ~49 hours | Resume pod 1 -> resume pod 2 (`76226b7abdb5`) | 7 | YES |

Cumulative: 58 hours, 17 anchors, 0 deviations.

### 14.3 Implication for IC-S23-2

NV persistence contract empirically strengthened. The IC-S23-2 contract is now grounded in 2 distinct cycle observations across 2 days. Stage 1+ may rely on NV-persisted artifacts surviving pod teardown without re-verification.

### 14.4 Status

CLOSED PASS. Recorded in `persistent_state.across_teardown_test_completed = true` and `persistent_state.bit_identity_preserved_across_cycles = true` in the reproducibility manifest.

## 15. OQ-S23-13 — RunPod Community Cloud Procurement Authorization

### 15.1 Question

Session 2.1 venue evaluation matrix specified Secure Cloud (primary) and Vast.ai (secondary fallback). RunPod's Community Cloud surfaced as a tertiary option during Session 2.3 capacity-unavailability event. Should it be added to the authorized venue list?

### 15.2 Trade-off

| Property | Secure Cloud | Community Cloud |
|---|---|---|
| Hardware vendor consistency | RunPod-validated datacenter | Third-party host hardware |
| Performance guarantees | RunPod SLA | "Performance unpredictable" per RunPod's own warning |
| Hourly rate | $0.69/hr (RTX 4090) | Variable (often lower) |
| Reproducibility provenance | Strong | Weak (host-dependent driver, network, uptime) |
| Capacity availability | Region-dependent; can exhaust | Generally higher availability |

### 15.3 Implication for Stage 1+

If Stage 1 SECT execution encounters consistent US-NC-1 Secure Cloud capacity constraints, the choice is between (a) waiting for capacity (indeterminate delay), (b) Vast.ai fallback (verified locked secondary), or (c) Community Cloud (currently unauthorized).

### 15.4 Forward routing

Session 2.5 Stage 1 prep cluster. Decision must be made before Stage 1 execution begins, not at point of capacity exhaustion.

If escalated to authorization: Community Cloud becomes tertiary fallback after Vast.ai. Manifest must record host fingerprint (driver version, GPU exact model, network egress characteristics) per Community Cloud pod.

If retained as excluded: Stage 1 must implement explicit wait-and-retry policy with operator-defined max wait time before falling to Vast.ai.

## 16. OQ-S23-14 — Duplicate Notebook at Workspace Root (NEW)

### 16.1 Question

A 47,027-byte notebook file `llm-as-database-agent-context-smoke-test.ipynb` is present at `/workspace/` root. Byte count matches `memit_dry_run/runpod_dry_run.ipynb`. The file was likely created during Block 2 by save-as-rename action on the original `Untitled.ipynb` before the canonical move into `memit_dry_run/`.

### 16.2 Disposition

| Question | Answer |
|---|---|
| Breaks reproducibility manifest? | No |
| Affects HC-2 verdict provenance? | No |
| Affects Block 3 directory layout commitment? | No |
| Affects rsync target size projection? | Negligible (+47 KB on top of 7.6 GB) |

### 16.3 Resolution candidates

```
A. Remove the duplicate (rm /workspace/llm-as-database-agent-context-smoke-test.ipynb)
B. Migrate into session_logs/ as session_2_3_block_2_notebook.ipynb
C. Retain as forensic evidence of pre-pause filesystem state
```

### 16.4 Forward routing

Session 2.4 prep, low priority. Operator's discretion. If retained, document its disposition in next session's startup state.

## 17. OQ-S23-15 — HF Cache Exclusion / MBP Headroom (CLOSED)

### 17.1 Question

If the rsync target were MBP-internal (20 GB free), Stage 2 sweep with LLaMA 3.1 8B HF cache (~16 GB) would force a cache exclusion decision. Should HF cache be excluded from the rsync mirror to preserve local disk headroom?

### 17.2 Resolution

External SSD selected as rsync target (Phase 5). Volume `memit` (APFS, 449.85 GB free at setup) relieves the headroom constraint entirely. HF cache exclusion is no longer required for capacity reasons.

### 17.3 Status

CLOSED as `not_applicable_external_drive_available`. The HF cache *location* decision (NV-backed vs container-disk) remains deferred under OQ-S23-5; only the *exclusion-from-mirror* question closes here.

## 18. OQ-S23-16 — RunPod Account-Level vs Pod-Level SSH Key Propagation (NEW)

### 18.1 Question

RunPod's account-level SSH key registration (Settings -> SSH Keys) does not propagate to pod-level `~/.ssh/authorized_keys` for newly-deployed pods. Why? Is this expected behavior, or did the key registration occur after pod deployment?

### 18.2 Empirical observation

During Phase 5 SSH auth attempt, pod `76226b7abdb5` had a pre-existing key (`SHA256:ZuzH58K...`) in `authorized_keys` that did not match the operator's MBP key. The operator manually appended their key to resolve auth.

### 18.3 Hypotheses

```
A. Account-level registration was applied AFTER this pod deployed
   (most likely)
B. RunPod's pod template baked in a different default key
C. The pre-existing pod-level key is a RunPod platform service key
   (possible; web terminal uses session tokens, not SSH)
```

### 18.4 Implication for Stage 1+

Manual `authorized_keys` injection is an unreliable workflow. Pre-deployment registration discipline must be established for Stage 1+ runbook authorship to avoid surprise auth failures on every new pod.

### 18.5 Forward routing

Session 2.5 Stage 1 prep. Mitigation patterns to evaluate:
- Add SSH key to RunPod account *before* deploying any pod intended for SSH/rsync access; verify propagation works.
- Embed `authorized_keys` injection in pod startup script (RunPod allows pod startup commands).
- Document pre-deployment key registration as a runbook precondition.

## 19. OQ-S23-17 — rsync Not Pre-Installed in `runpod/pytorch:2.4.0` (CLOSED)

### 19.1 Question

The `runpod/pytorch:2.4.0` image does not pre-install `rsync`. Phase 5 initial sync attempt failed with `rsync: command not found` on the pod side.

### 19.2 Resolution

`apt-get install -y rsync` executed on pod. Installed rsync 3.2.7, protocol version 31. Phase 5 initial sync re-executed successfully.

### 19.3 Status

CLOSED. The constraint is now codified as C-S23-5 in the Session Summary Block.

### 19.4 Forward routing

Stage 1+ runbooks must include `apt-get install -y rsync` as a Step 0 precondition before any rsync-dependent operation. Add to `block-2-3-runbook-deltas.md` Section 12 system-binary dependency manifest.

## 20. OQ-S23-18 — skopeo Not Pre-Installed in `runpod/pytorch:2.4.0` (CLOSED)

### 20.1 Question

The `runpod/pytorch:2.4.0` image does not pre-install `skopeo`. Block 2 image digest verification required `apt-get install -y skopeo` at session start.

### 20.2 Resolution

`apt-get install -y skopeo` executed at Block 2 verification time. skopeo 1.4.1 installed and operational; image digest reconciliation against Docker Hub successful.

### 20.3 Status

CLOSED. The constraint is now codified as C-S23-6 in the Session Summary Block.

### 20.4 Forward routing

Stage 1+ runbooks must include `apt-get install -y skopeo` as a Step 0 precondition for any session that requires image digest verification. Co-located with OQ-S23-17 in runbook deltas Section 12.

## 21. OQ-S23-19 — RunPod Web Terminal Paste-Buffer Ceiling (NEW)

### 21.1 Question

RunPod's web terminal has a paste-buffer ceiling that truncates pastes above approximately 5,000 characters. Phase 6 manifest write (8,195 bytes) failed via direct paste; required SSH-pipe-from-MBP via rsync to complete.

### 21.2 Empirical observation

Bash heredoc paste of ~10,000 character Python content truncated mid-stream at the `runpod_dry_run.completed_at` field. Subsequent re-attempt at smaller scope succeeded. Phase 7 Session Summary Block (12,153 bytes) used SSH-pipe-from-MBP method preemptively to avoid recurrence.

### 21.3 Implication for Stage 1+

Stage 1+ runbooks should NOT assume large literal-block pastes work via the pod's web terminal. For artifacts larger than ~3,000 characters, use one of:

```
A. SSH-pipe-from-MBP: ssh ... 'cat > /workspace/file' < /tmp/file_on_mbp
B. rsync push: rsync -avz /tmp/file ssh://pod:/workspace/
C. scp push: scp -P PORT /tmp/file root@IP:/workspace/
D. Multi-part heredoc: split into chunks under the ceiling
```

### 21.4 Forward routing

Stage 1 runbook authorship (Session 2.5). Add to runbook deltas as a Tooling section. May benefit from a small helper script in `~/scripts/` on MBP for SSH-pipe-from-MBP pattern.

## 22. Forward-Routing Summary

```
Resume of Session 2.3 (CLOSED PASS):
  - OQ-S23-3, 12, 15, 17, 18 closed (5 closures)

Session 2.4 (CFB v1 + probe-set authorship):
  - OQ-S23-6 (token-id source discipline) applies during probe authorship
  - OQ-S23-14 (duplicate notebook) low-priority disposition

Session 2.5 (Stage 1 SECT execution prep):
  - OQ-S23-1 closes or routes to manual monitoring
  - OQ-S23-5 closes (HF cache strategy)
  - OQ-S23-13 closes (Community Cloud procurement)
  - OQ-S23-16 closes (SSH key registration timing)

Stage 1+ runbook authorship (consolidated in Session 2.5):
  - OQ-S23-2 (manifest discipline)
  - OQ-S23-4 (import-time dep closure)
  - OQ-S23-6 (token-id source discipline)
  - OQ-S23-7 (Cell 3 idempotence)
  - OQ-S23-8 (failure mode taxonomy)
  - OQ-S23-9 (diagnostic logging variance)
  - OQ-S23-19 (paste ceiling discipline)

MEMIT fork (OQ-S22-17 future task):
  - OQ-S23-10 (past_key_values Cache API migration)

Workstream 3 implementation planning:
  - OQ-S23-11 (.vindex bit-identity spec elevation)
```

All OQ-S23-* entries are tracked through to closure. None are abandoned.
