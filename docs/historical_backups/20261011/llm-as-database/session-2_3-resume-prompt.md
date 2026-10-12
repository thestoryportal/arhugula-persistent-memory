/memit-specialist
/aiSecOps-specialist (secondary)

<session_context>
Workstream 1, Session 2.3 — Block 2 RunPod Activation and Block 3 Persistent
State Architecture.

Predecessor: Session 2.2 closed with Kaggle Block 1 smoke test PASS verdict
on 2026-04-26. The reproducibility manifest seed is captured in
architecture-profile-seed.json. Six MEMIT patches are documented and
universal vs conditional status established. Block 2 (RunPod activation)
is authorized.

All operator decisions remain locked from Session 2.1 and Session 2.2:
  - Production target: LLaMA 3.1 8B
  - Calibration baseline: GPT-J 6B (smoke test PASS confirmed)
  - Primary venue: RunPod Secure Cloud RTX 4090 on-demand at $0.69/hr
  - Stage 2 sweep: on-demand, no preemption
  - Persistent state: 100 GB RunPod Network Volume + local rsync to 2020 MBP
  - Apple Silicon: rejected for POC
  - MEMIT pin: SHA 80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b
  - Joint pin: transformers 4.45.2 + accelerate 0.34.2 + huggingface_hub 0.25.2
  - GPT-J 6B revision: float16, SHA b71ae8bc86cac13154e03e92b5855203086b722e
  - Required patches for RTX 4090: P-1, P-2, Pad-Token, Copy-Unmount
  - Patches NOT required for RTX 4090: P-3', Explicit device map

Output is execution records and the finalized reproducibility manifest, not
new specification work. The session ends with HC-2 PASS, NV provisioned,
directory layout committed, rsync configured, and Session Summary Block
emitted.
</session_context>

<task>
Walk the operator through five sequential blocks of work, in order:

1. RunPod account provisioning (Step 2.1). Account creation, payment
   method, billing alerts at $50, $150, $300 thresholds.

2. Network Volume provisioning (Step 2.2). Region selection (verify RTX
   4090 capacity availability before creating NV). 100 GB allocation.
   Mount-verification via cheapest-tier test pod. Test pod teardown.

3. PyTorch container image selection (Step 2.3). Browse RunPod's catalog,
   select an image matching constraints (PyTorch 2.x ≥ 2.0,
   CUDA 12.x, Python 3.10/3.11, supports register_forward_hook
   with_kwargs=True). Pin by SHA256 digest, not tag. Compatibility test
   on a minimal pod.

4. Dry-run pod with HC-2 reproduction (Step 2.4). Spin up RTX 4090 pod
   with NV mounted; execute the 10-cell RunPod canonical notebook from
   block-2-runpod-notebook.md. Compare numerical metrics against the
   Kaggle baseline. HC-2 PASS criterion: SF-1, SF-2, SF-3 all PASS AND
   drift_p_baseball_post < 0.05 AND drift_p_basketball_post < 10 AND
   drift_p_basketball_postunmount < 1e-6.

5. Block 3: Persistent state architecture (Steps 3.1–3.3). Commit
   directory layout on NV. Configure rsync from RunPod NV to operator's
   MacBook Pro local archive. Finalize architecture-profile-seed.json
   with runpod_dry_run, persistent_state, and rsync_target fields
   populated.

The session is hands-on. Claude provides navigation: which steps to run,
what to verify, what to halt on. The operator runs the actual commands
on their machine and RunPod console. Payment data and account credentials
do not enter the chat.
</task>

<inputs>
- block-2-execution-plan.md: full Block 2 step-by-step runbook
- block-2-runpod-notebook.md: 10-cell canonical notebook for RunPod RTX 4090
- memit-patches-canonical.md: six patches with exact text and application order
- architecture-profile-seed.json: reproducibility manifest seed from Block 1
- session-2_2-summary-block.md: predecessor session record
- memit-compat-proto-1.md: HC-2 specification context
- GPU procurement analysis: NV cost (~$7/month at $0.07/GB/month)
- llm-as-database-v1_2-integrated-spec.md Appendix A: deployment preconditions
</inputs>

<hc_2_acceptance_band>
HC-2 (the Kaggle vs RunPod numerical comparison) PASSES if all of the
following hold:

  - SF-1: post-edit top-1 == 'baseball' on RunPod
  - SF-2: P(baseball) > P(basketball) post-edit on RunPod
  - SF-3: post-unmount top-1 == 'basketball' on RunPod
  - |P_baseball_post_runpod - 0.9819| / 0.9819 < 0.05
    (within 5% of Kaggle baseline)
  - |P_basketball_post_runpod - 2.30e-04| / 2.30e-04 < 10
    (within order of magnitude of Kaggle baseline)
  - |P_basketball_postunmount_runpod - 0.8702| / 0.8702 < 1e-6
    (bit-identical overlay isolation; tighter band)

A FAIL on any element halts the session. RunPod activation does not
proceed to Stage 1 until HC-2 PASSes. Material drift (>5% on
P_baseball_post or worse than bit-identical on overlay isolation)
indicates environment-specific MEMIT behavior worth investigating.
</hc_2_acceptance_band>

<method>
Block 2 (Steps 2.1–2.5) follows block-2-execution-plan.md sections 3–7.
Block 3 (Steps 3.1–3.3) follows the §3 directory layout from session-2.2
prompt, with rsync configuration per §3.2 of that prompt.

# Block 2 — Execute in order

1. Account provisioning (block-2-execution-plan §3).
   - Operator creates RunPod account, adds payment method, configures
     billing alerts. Reports back: verification status, payment method
     confirmed (yes/no), billing alerts configured (yes/no), any account
     flags.

2. Network Volume provisioning (block-2-execution-plan §4).
   - Operator confirms RTX 4090 Secure Cloud capacity in target region
     BEFORE creating NV. Recommended region order: US-OR-1, US-KS-2,
     US-TX-3, EU-RO-1.
   - Create 100 GB NV in selected region.
   - Spin up cheapest-tier test pod (e.g., RTX A4000) with NV mounted at
     /workspace; verify mount, write, size, region.
   - Tear down test pod.
   - Reports back: NV ID, region, mount verdict.

3. Container image selection (block-2-execution-plan §5).
   - Operator browses RunPod catalog (Pods → Templates → PyTorch).
   - Select image matching: PyTorch 2.x (≥ 2.0; with_kwargs hook supported),
     CUDA 12.x, Python 3.10 or 3.11.
   - Pin by SHA256 digest, not tag.
   - Compatibility test (per block-2-execution-plan §5.4) on minimal pod.
   - Reports back: image reference, digest, compatibility verdict.

4. Dry-run pod and HC-2 reproduction (block-2-execution-plan §6).
   - Spin up 1× RTX 4090 Secure Cloud pod with NV mounted at /workspace
     and pinned image.
   - Execute 10-cell canonical notebook from block-2-runpod-notebook.md.
   - Cell 6 wall time expectation: ~3-5 min on RTX 4090 (vs ~7-8 min on
     Kaggle T4 with CPU solve).
   - Cell 10 emits HC-2 verdict against Kaggle baseline.
   - Halt if HC-2 FAIL.

5. Pod teardown and NV persistence verification (block-2-execution-plan §7).
   - Save runpod_dry_run_verdict.json to NV.
   - Tear down dry-run pod.
   - Spin up second cheap pod with NV mounted; verify dry_run_verdict.json
     readable. Tear down.
   - Reports back: NV persistence verdict.

# Block 3 — Persistent state architecture and reproducibility manifest

1. Network Volume directory layout (per Session 2.2 prompt §3 in
   block-2-execution-plan §10 reference structure):
     /workspace/
       architecture_profile/        # PF-1..PF-6 outputs at Stage 1
       vindex_overlays/              # MEMIT edit overlays per stage
       cfb_baseline/                 # CFB v1 corpus + pre-edit baseline
       covariance_caches/            # PF-5 covariance matrices, hashed
       drift_sweep_results/          # Stage 2 outputs
       epsilon_calibration/          # Stage 3a outputs
       compaction_probe_calibration/ # Stage 3b outputs
       judge_calibration/            # Stage 3c outputs
       reproducibility_manifest.json # the pinned-version record
       session_logs/                 # per-session execution logs

   Confirm or adjust with operator. Commit by creating empty directories.

2. Local rsync configuration on MacBook Pro:
   - Identify local target directory.
   - Confirm available local disk (rough estimate: 100 GB headroom).
   - Walk through rsync command syntax for weekly mirror.
     Sample command pattern:
       rsync -avz --delete \
           runpod:/workspace/ \
           /Users/<operator>/llm-database-poc-mirror/
   - Note: rsync target is backup, not source of truth. NV is source of
     truth during POC.

3. Compose finalized reproducibility manifest by populating Block 2
   fields in architecture-profile-seed.json:
   - runpod_dry_run.pod_image_digest
   - runpod_dry_run.completed_at
   - runpod_dry_run.edit_success_metric (Cell 10 verdict)
   - runpod_dry_run.drift_from_kaggle (HC-2 drift values)
   - persistent_state.network_volume_id
   - persistent_state.network_volume_region
   - persistent_state.directory_layout_committed (true)
   - rsync_target.local_path
   - rsync_target.cadence ("weekly")

4. Save finalized manifest to NV at:
   /workspace/reproducibility_manifest.json

5. Compose Session 2.3 Summary Block.
</method>

<output_format>
Produce a single markdown document at session end with these sections,
in order:

## Bottom Line
Two-sentence summary: HC-2 verdict; persistent state state; whether Stage
1 is authorized.

## Block 2 — Execution Record
Step-by-step record of Steps 2.1 through 2.5. Each step's deliverable
and any deviations from the planned protocol.

## Block 3 — Persistent State and Reproducibility Manifest
Final NV directory layout (committed); rsync target configuration;
finalized reproducibility manifest as JSON.

## HC-2 Drift Report
Numerical comparison: Kaggle baseline vs RunPod measured. Per-metric
drift values and band assessment.

## Open Questions / Carry-Forward to Stage 1
Anything observed during Block 2 / Block 3 that informs Stage 1
planning.

## Halt Notice (only if session halted)
What was attempted; where it failed; what to diagnose; what next session
should re-open.

## Session Summary Block
Standard format. Decisions made / Constraints established / Open
questions deferred / Interface contracts defined / Next session
candidates.
</output_format>

<constraints>
- Do NOT execute commands on behalf of the operator. Claude is the
  navigator. The operator runs the commands on their own machine and
  in the RunPod console.
- Do NOT have the operator paste API keys, payment information, or
  account credentials into the chat.
- Do NOT default to "latest" tags. Pin every container image by SHA256
  digest. The reproducibility manifest depends on this discipline.
- Do NOT skip the dry-run pod. HC-2 is the load-bearing checkpoint
  before Stage 1 SECT execution. Even if RunPod responds and the model
  loads, the numerical comparison to Kaggle must run.
- Do NOT begin Stage 1 SECT (3 facts × 3 runs) in this session. The
  dry-run is one fact, one run.
- Do NOT begin probe-set v1 or CFB v1 authorship.
- Do NOT begin LLaMA 3.1 8B work. The dry-run uses GPT-J 6B (calibration
  baseline; same as Kaggle smoke test) for direct numerical comparison.
- If a verification step surfaces an environment incompatibility,
  surface it as an open question. Do not work around silently.
- HC-2 drift band is non-negotiable. Drift outside the band halts the
  session.
</constraints>

<stopping_rule>
Session is complete when ONE of the following holds:

1. Successful path: HC-2 PASS; RunPod NV provisioned; container image
   digest pinned; dry-run pod torn down with NV persistence verified;
   NV directory layout committed; rsync configured; reproducibility
   manifest finalized; Session Summary Block produced.

2. Halt path: any halt condition triggered; halt notice recorded;
   Session Summary Block produced with halt reason and diagnosis next-step.

The session does NOT proceed to Stage 1 SECT execution, full
architecture_profile.json drafting against LLaMA 3.1 8B, CFB v1
authorship, or probe-set v1 authorship. Each is its own session.
</stopping_rule>

# Session 2.3 Resume — Orientation for Next Agent

## 1. Purpose

This document orients a fresh agent context to resume Session 2.3 mid-stream. Session 2.3 paused after Block 2 (HC-2 PASS verdict locked) and before Block 3 (persistent state architecture). The pause was a sleep break; resume context is identical to pre-pause except no GPU pod is running.

## 2. Read Order for Next Agent

| Priority | Document | Purpose |
|---|---|---|
| 1 | `session-2_3-resume-prompt.md` (this file) | Orientation and resume sequence |
| 2 | `session-2_3-partial-summary.md` | What was accomplished; HC-2 verdict; current state |
| 3 | `block-3-resume-execution-plan.md` | What to execute on resume |
| 4 | `block-2-3-runbook-deltas.md` | Spec amendments discovered during execution; future runbook constraints |
| 5 | `oq-s23-backlog.md` | All 13 open questions logged this session |

The original Session 2.3 prompt should also be re-supplied to the next agent verbatim. This package augments — does not replace — that prompt.

## 3. Session State at Pause

### 3.1 Block-level status

| Block | Step | Status |
|---|---|---|
| Block 2 | 2.1 Account provisioning | CLOSED |
| Block 2 | 2.2 NV provisioning + mount verification | CLOSED |
| Block 2 | 2.3 Image digest pinning | CLOSED |
| Block 2 | 2.4 Dry-run pod + HC-2 reproduction | **PASS** |
| Block 2 | 2.5a Final artifact audit on GPU pod | CLOSED |
| Block 2 | 2.5b GPU pod termination | CLOSED |
| Block 2 | 2.5c Cheap pod spin-up | NOT STARTED (US-NC-1 capacity unavailable) |
| Block 2 | 2.5d Across-teardown NV persistence test | DEFERRED → executes naturally on resume's new pod mount |
| Block 3 | 3.1 Directory layout commit | NOT STARTED |
| Block 3 | 3.2 rsync configuration | NOT STARTED |
| Block 3 | 3.3 Manifest finalization | NOT STARTED |
| Session | Summary Block emission | NOT STARTED |

### 3.2 HC-2 Verdict

```
verdict:        PASS
hc_2_verdict:   PASS
SF-1, SF-2, SF-3:                                       all PASS
drift_p_baseball_post:                  1.28e-3   band: 0.05    PASS
drift_p_basketball_post:                0.480     band: 10      PASS
drift_p_basketball_postunmount_intrapod: 0.0      band: 1e-4    PASS
drift_p_basketball_postunmount_crossenv: 4.65e-4  informational
```

Verdict file: `/workspace/memit_dry_run/runpod_dry_run_verdict.json` (2,655 bytes; on NV `large_amethyst_wolverine`).

### 3.3 Pod state

```
GPU pod aesthetic_emerald_wallaby (RTX 4090, US-NC-1):  TERMINATED
NV large_amethyst_wolverine:                            DETACHED, intact
NV size used:                                           7.6 GB / 100 GB
NV cost during pause:                                   ~$0.01/hr storage only
```

### 3.4 Capacity context at pause

US-NC-1 reported all GPU types out of stock at pause time. RunPod Community Cloud RTX 5000 was offered and rejected (Session 2.1 venue lock; OQ-S23-13). Capacity at resume is unknowable; first action on resume is capacity check.

## 4. Resume Sequence (High-Level)

```
                ┌──────────────────────────────────────────────┐
                │ 1. Capacity check: RTX 4090 in US-NC-1       │
                │    (fallback: RTX 5090; reject Community)    │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                ┌──────────────────────────────────────────────┐
                │ 2. Deploy pod with pinned image digest       │
                │    NV large_amethyst_wolverine at /workspace │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                ┌──────────────────────────────────────────────┐
                │ 3. Step 2.5d: NV persistence test            │
                │    (executes naturally on first mount)       │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                ┌──────────────────────────────────────────────┐
                │ 4. Step 3.1: Directory layout commit         │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                ┌──────────────────────────────────────────────┐
                │ 5. Step 3.2: rsync configuration             │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                ┌──────────────────────────────────────────────┐
                │ 6. Step 3.3: Manifest finalization           │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                ┌──────────────────────────────────────────────┐
                │ 7. Session Summary Block emission            │
                │    Pod terminate; session 2.3 closes         │
                └──────────────────────────────────────────────┘
```

Detailed execution steps: `block-3-resume-execution-plan.md`.

## 5. Pinned Decisions (Carry from Session 2.1 / 2.2 / 2.3)

These are non-negotiable; the next agent must preserve all values.

| Decision | Value | Locked in |
|---|---|---|
| Production target model | LLaMA 3.1 8B | Session 2.1 |
| Calibration baseline model | GPT-J 6B | Session 2.1 |
| Primary venue | RunPod Secure Cloud RTX 4090 on-demand | Session 2.1 |
| Hourly rate | $0.69/hr | Session 2.1 |
| Stage 2 sweep | On-demand, no preemption | Session 2.1 |
| Persistent state | 100 GB RunPod NV + local rsync to MBP | Session 2.1 |
| Apple Silicon | Rejected | Session 2.1 |
| Community Cloud | Rejected (OQ-S23-13 deferred to Session 2.5) | Session 2.3 |
| MEMIT pin SHA | `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` | Session 2.2 |
| Joint version pin | transformers 4.45.2 + accelerate 0.34.2 + huggingface_hub 0.25.2 | Session 2.2 |
| GPT-J 6B revision | `float16`, SHA `b71ae8bc86cac13154e03e92b5855203086b722e` | Session 2.2 |
| Container image | `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` | Session 2.3 |
| Image digest | `sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5` | Session 2.3 |
| Runtime PyTorch | 2.4.1+cu124 (image patch-level differs from tag — see OQ-S23-2) | Session 2.3 |
| Runtime Python | 3.11.10 | Session 2.3 |
| Runtime CUDA (torch) | 12.4 | Session 2.3 |
| Runtime CUDA (driver) | 12.8 (driver 570.195.03) | Session 2.3 |
| GPU compute capability | sm_89 (RTX 4090 Ada Lovelace) | Session 2.3 |
| Region | US-NC-1 (NV-pinned) | Session 2.3 |
| Patches required (RunPod) | P-1, P-2, Pad-Token, Copy-Unmount | Session 2.2/2.3 |
| Patches NOT required (RunPod) | P-3', Explicit device map | Session 2.2/2.3 |
| Datasets pin | `datasets==4.8.3` (Kaggle parity) | Session 2.3 |
| Additional MEMIT deps | matplotlib 3.9.2, scipy 1.14.1, pandas 2.2.3, sklearn 1.5.2 | Session 2.3 |
| NV ID/name | `large_amethyst_wolverine` | Session 2.3 |
| NV mount path | `/workspace` | Session 2.3 |
| Working directory | `/workspace/memit_dry_run/` | Session 2.3 |

## 6. NV Artifact Inventory (Pre-Resume State)

These artifacts persist on NV and survive teardown; resume's NV persistence test verifies their continued presence.

| Path | Size | Purpose |
|---|---|---|
| `/workspace/memit_dry_run/runpod_dry_run.ipynb` | 47,027 B | Block 2 execution record (notebook source) |
| `/workspace/memit_dry_run/runpod_dry_run_verdict.json` | 2,655 B | HC-2 PASS verdict (load-bearing) |
| `/workspace/memit_dry_run/smoke_test_overlay/edited.pt` | 805,308,606 B | MEMIT-edited weight overlay |
| `/workspace/memit_dry_run/smoke_test_overlay/original.pt` | 805,309,074 B | Pre-edit weight backup |
| `/workspace/memit_dry_run/memit/` (patched clone) | ~25 MB + cache | MEMIT codebase with P-1+P-2 patches applied |
| `/workspace/memit_dry_run/memit/util/nethook.py` | 15,708 B | P-1+P-2 patched (with_kwargs=True; arg synthesis) |
| `/workspace/memit_dry_run/memit/data/stats/EleutherAI_gpt-j-6B/wikipedia_stats/` | 6.1 GB | Covariance cache for layers 3-8 |
| `/workspace/memit_dry_run/.ipynb_checkpoints/` | small | Notebook autosave history |
| `/workspace/.ipynb_checkpoints/` | small | Unrelated operator notebook checkpoints (not part of Block 2) |
| `/workspace/Untitled.ipynb` would be | absent | Was moved to `/workspace/memit_dry_run/runpod_dry_run.ipynb` pre-pause |
| **Total NV used** | **7.6 GB / 100 GB** | |

## 7. Cost Tracker

| Item | Estimate |
|---|---|
| Block 2 GPU pod cumulative (terminated) | ~$1.65 |
| NV storage during pause (~7 hr) | ~$0.07 |
| Resume pod (RTX 4090, ~30-40 min) | ~$0.40 |
| **Block 2 + 3 total projection** | **~$2.12** |
| Block 2 burst budget | $5.00 |
| Headroom | ~$2.88 |

## 8. Critical Operator Behaviors to Preserve

The next agent must apply these:

| Behavior | Source |
|---|---|
| Capacity verify BEFORE deploy (US-NC-1 only; NV region-pinned) | Block 2 lessons |
| Image pin by SHA256 digest, never tag | Reproducibility manifest discipline |
| Defer non-Path-C alternatives unless explicitly authorized | Session 2.1 venue lock |
| Operator runs commands; agent navigates only | Session prompt §<constraints> |
| No payment data, credentials, or API keys in chat | Session prompt §<constraints> |
| Halt on HC-2 acceptance band failure | Session prompt §<hc_2_acceptance_band> |
| Surface, do not work around, environment incompatibilities | Session prompt §<constraints> |
| C extension version mismatches require kernel restart (not in-place retry) | OQ-S23-8 (this session) |
| MEMIT import-time deps require exhaustive single-cell install (not discovery-by-failure) | OQ-S23-4 (this session) |

## 9. Session 2.3 Closure Criteria (Restated)

Session 2.3 closes successfully on **all** of:

- HC-2 PASS (already achieved; locked in verdict JSON on NV)
- RunPod NV provisioned (already complete)
- Container image digest pinned (already complete)
- Dry-run pod torn down with NV persistence verified (NV persistence verification deferred to resume's pod mount; halt criterion if mount loses content)
- NV directory layout committed (Step 3.1 — pending)
- rsync configured (Step 3.2 — pending)
- Reproducibility manifest finalized (Step 3.3 — pending)
- Session Summary Block produced (final action — pending)

Five of eight criteria are already met. Three pending steps + summary closure remain.

## 10. Forward Pointers

After Session 2.3 closes, the immediate downstream sessions are:

| Session | Topic | Blocked on |
|---|---|---|
| 2.4 | CFB v1 corpus authorship + probe-set v1 authorship | Session 2.3 closure |
| 2.5 | Stage 1 SECT execution prep + LLaMA 3.1 8B target model commitment | Session 2.4 closure (or partial; some prep is path-independent) |

OQ-S23-12 (across-teardown NV persistence test) will close on resume's first mount. OQ-S23-13 (Community Cloud procurement) carries to Session 2.5 prep.

All other OQ-S23-* entries are runbook-authorship constraints for Stage 1+ runbooks; they do not gate Session 2.4 or 2.5 startup.
