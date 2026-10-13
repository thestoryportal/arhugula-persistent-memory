# Session 2.3 — Entry Note and Session Prompt

> **Workstream:** 1 — Empirical POC Scoping (post-v1.2 sealed spec)
> **Session:** 2.3 — Block 2 RunPod Activation and Block 3 Persistent State Architecture
> **Position in arc:** Opens after Session 2.2 (Block 1 Kaggle smoke test PASS verdict).
> **Primary skill:** `memit-specialist`
> **Secondary skill:** `aiSecOps-specialist` (Warden — tenant isolation, audit posture, billing safety)

---

## Session Character — Read Before Beginning

This session continues the execution-shape arc from Session 2.2. The Kaggle smoke test (Block 1) closed with verdict PASS on 2026-04-26. RunPod activation is now authorized.

The session walks through:

- RunPod account creation, payment method, billing alerts (Step 2.1)
- Network Volume provisioning with region pinning (Step 2.2)
- PyTorch container image selection and digest pinning (Step 2.3)
- Dry-run pod with single-fact MEMIT reproduction; HC-2 numerical comparison to Kaggle (Step 2.4)
- Pod teardown and NV persistence verification (Step 2.5)
- Block 3: Persistent state directory layout, rsync configuration to operator's MacBook Pro, finalized reproducibility manifest (Steps 3.1–3.3)

The session does NOT include: Stage 1 SECT execution (3 facts × 3 runs against LLaMA 3.1 8B), CFB v1 corpus authorship, probe-set v1 authorship, or full architecture_profile.json drafting against the production target. Those are separate Stage 0 / Stage 1 sub-sessions.

## Operator Decisions Locked from Session 2.2

These are settled. Do not re-deliberate:

- **Production target:** LLaMA 3.1 8B (per Session 2.0)
- **Calibration baseline:** GPT-J 6B (per Session 2.0; smoke test PASS confirmed)
- **Primary procurement venue:** RunPod Secure Cloud RTX 4090 ($0.69/hr on-demand)
- **Secondary cost-floor venue:** Vast.ai Secure DC RTX 4090 (capacity fallback only)
- **Stage 2 sweep tier:** On-demand (no preemption)
- **Persistent storage:** 100 GB Network Volume on RunPod
- **Local archive:** rsync to existing 2020 Intel MBP 16 GB
- **Apple Silicon:** rejected for POC
- **MEMIT toolchain pin:** SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`
- **Joint version pin:** transformers 4.45.2, accelerate 0.34.2, huggingface_hub 0.25.2, tokenizers 0.20.3, safetensors 0.4.5
- **GPT-J 6B revision:** `float16` revision SHA `b71ae8bc86cac13154e03e92b5855203086b722e`
- **Required patches for RTX 4090:** P-1 + P-2 (nethook), Pad-Token alias, Copy-Unmount
- **Patches NOT required for RTX 4090:** P-3' (CPU FP64 solve), Explicit device map

## KB Curation for This Session

Re-add these documents to the KB; remove non-relevant Session 2.2 artifacts:

| Document | Role in this session |
|---|---|
| `session-2_2-summary-block.md` | Authoritative carry-forward from prior session |
| `architecture-profile-seed.json` | Reproducibility manifest seed; Block 2 dry-run appends |
| `memit-patches-canonical.md` | Six patches with exact text and application order |
| `block-2-execution-plan.md` | Block 2 operator runbook (load-bearing for this session) |
| `block-2-runpod-notebook.md` | 10-cell canonical notebook for RunPod RTX 4090 |
| `kaggle-canonical-notebook.md` | Reference artifact (do not re-execute) |
| `memit-compat-proto-1.md` | Re-add for HC-2 comparison context |
| `GPU_Procurement_for_LLM-as-Database_POC__Cloud_Rental_vs_Apple_Silicon_Analysis.md` | Re-add for §6 / Network Volume cost reference |
| `MEMIT_Target_Model_Recommendation__Survey_of_Eleven_Open-Weights_Candidates.md` | Re-add for LLaMA 3.1 8B production target context |
| `write-engine-poc-scope.md` | Re-add for Block 3 persistent state context |
| `poc-execution-plan-and-spec-revision-rule.md` | Re-add for reproducibility discipline |
| `llm-as-database-v1_2-integrated-spec.md` | Re-add for Appendix A deployment preconditions |

## Documents NOT in the KB for this session

- `kaggle-canonical-notebook.md` is reference-only; do not load full content unless an operator question requires it
- Stage 2 / Stage 3 protocols (`memit-drift-proto-1.md`, `epsilon-calib-proto-1.md`, `compaction-probe-calib-proto-1.md`, `judge-calib-proto-1.md`) — re-add at Stage 1 kickoff, not this session
- `tension-map-v5.md`, `gap-backlog-v5.md` — neither has direct Block 2 / Block 3 relevance

## Tools Expected in This Session

- **Web search and web fetch** — for current RunPod container image catalog state, current RTX 4090 capacity by region, current PyTorch image digests
- **No code execution by Claude** — operator runs all commands on their machine, RunPod console, and the dry-run pod. Claude is the navigator
- **Past conversation search** — for retrieving Session 2.2 specifics if needed

## Output Discipline

The session produces **execution records and the final reproducibility manifest**. Specifically:

1. **Block 2 outputs:**
   - Account state record (verification status, payment method confirmed, billing alerts at $50/$150/$300)
   - NV provisioning record (NV ID, region, mount-test verdict)
   - Container image record (full image reference, SHA256 digest, compatibility test verdict)
   - Dry-run pod verdict JSON (`runpod_dry_run_verdict.json` per `block-2-runpod-notebook.md` Cell 10)
   - HC-2 numerical drift report (Kaggle vs RunPod comparison)

2. **Block 3 outputs:**
   - Network Volume directory layout committed
   - Local rsync configuration on MacBook Pro
   - Finalized `architecture-profile-seed.json` with `runpod_dry_run`, `persistent_state`, `rsync_target` populated
   - Session 2.3 Summary Block

The session does NOT:

- Execute Stage 1 SECT
- Author CFB v1 corpus or probe-set v1
- Draft full architecture_profile.json against LLaMA 3.1 8B (PF-1 through PF-6 against production target are Stage 1 work)

## Stopping Conditions

Session ends successfully when:

- Block 2 Steps 2.1–2.5 all complete; HC-2 PASS
- Block 3 directory layout committed; rsync configured; manifest finalized
- Session Summary Block authored; Stage 1 authorization recorded

Session ends with HALT (do not proceed to Block 3) if:

- RunPod account verification fails or billing alerts cannot be configured
- NV cannot be provisioned (capacity unavailable across all candidate regions)
- All candidate container images fail compatibility test
- HC-2 numerical drift exceeds band (>5% on `P_baseball_post`, or any SF assertion FAILs on RunPod)
- Block 2 cost exceeds $5 (cost runaway indicator)

A halt is not a failure — it surfaces a constraint that requires resolution before Stage 1 SECT can begin.

---

*Entry note ends. The fresh session prompt follows below.*

---

## Session 2.3 — Prompt

```
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
```

---

*End of Session 2.3 entry note and prompt.*
