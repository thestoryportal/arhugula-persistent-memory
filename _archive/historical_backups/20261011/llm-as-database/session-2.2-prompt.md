# Session 2.2 — Procurement Execution and Kaggle Smoke Test Prompt

> Paste the prompt below into a new chat session **after** the entry note has been read. The prompt assumes the project's revised system prompt is in place and the curated KB (6 documents) is loaded. This session is execution-shape, not recommendation-shape — Claude is the navigator walking the operator through hands-on steps, not the agent doing the work.

---

```
/memit-specialist
/aiSecOps-specialist (secondary)

<session_context>
Workstream 1, Session 2.2 — Procurement Execution and Kaggle Smoke Test.
Last Stage 0 prep session before Stage 1 (MEMIT-COMPAT-PROTO-1) execution.

All operator decisions are locked from prior sessions:
  - Production target: LLaMA 3.1 8B
  - Calibration baseline: GPT-J 6B
  - Primary venue: RunPod Secure Cloud RTX 4090 on-demand at $0.69/hr
  - Stage 2 sweep: on-demand, no preemption
  - Smoke test discipline: Kaggle first; no paid activation until smoke passes
  - Persistent state: 100 GB RunPod Network Volume + local rsync to 2020 MBP
  - Apple Silicon: rejected for POC

Output is an execution record, not a recommendation. The session ends with
a smoke test verdict, a reproducibility manifest, and a provisioning state
record.
</session_context>

<task>
Walk the operator through three sequential blocks of work:

1. Kaggle smoke test setup and execution. Confirm the MEMIT toolchain
   runs cleanly on a free-tier CUDA environment by reproducing one
   published CounterFact edit against GPT-J 6B.
2. RunPod activation, conditional on smoke test passing. Provision the
   account, payment method, Network Volume, and a dry-run pod.
3. Persistent state architecture and reproducibility manifest. Define
   the directory layout on the Network Volume, the local rsync target
   on the MacBook Pro, and the pinned-version manifest that anchors
   the eventual architecture_profile.json.

The session is hands-on. Claude provides the navigation: which steps
to run in which order, what to verify at each checkpoint, what success
and failure look like, what to halt on. The operator runs the actual
commands on their machine and on Kaggle / RunPod.
</task>

<inputs>
- Smoke test protocol guidance: project KB, GPU procurement analysis §6
  ("Free-tier pre-flight smoke test: Kaggle Notebooks") and the smoke
  test description in §9 session summary.
- Pre-flight requirements being rehearsed: project KB, memit-compat-proto-1.md
  PF-1 through PF-6. The smoke test is a single-fact miniature of SECT
  (memit-compat-proto-1.md §3) — it does NOT execute the full SECT.
- Target model VRAM requirements: project KB, target model recommendation
  document. GPT-J 6B FP16 ≈ 12 GB; LLaMA 3.1 8B FP16 ≈ 16 GB.
- Persistent state requirements: project KB, llm-as-database-v1_2-integrated-spec.md
  Appendix A — single OS user, filesystem privacy, persistent storage.
- MEMIT reference repository: kmeng01/memit on GitHub. Verify current
  state via web_fetch before walking through. The repository's
  hparams/MEMIT/EleutherAI_gpt-j-6B.json is the canonical starting
  configuration for the smoke test.
- CounterFact reference numbers: published in the original MEMIT paper
  (arXiv:2210.07229, Meng et al.) and reproduced in subsequent papers.
  Operator will validate against one published reference fact, not the
  full CounterFact corpus.
</inputs>

<smoke_test_specification>
The smoke test is the load-bearing checkpoint for this session. It is
NOT the full Stage 1 SECT. It is a single-fact rehearsal that confirms:

- The Kaggle CUDA environment supports MEMIT's PyTorch version requirements.
- GPT-J 6B downloads and converts to FP16 within Kaggle's session limits.
- MEMIT's covariance precomputation step succeeds on at least one MLP layer
  without divergence or NaN (a miniature PF-5).
- One MEMIT edit on one published CounterFact reference fact succeeds with
  L1 storage probe (read-back of the edited fact) returning the expected
  target token.
- The edited overlay can be unmounted and the pre-edit response returns
  (a miniature SECT step 6 — overlay isolation check).

Pass criteria:
- L1 storage probe returns expected target on the edited fact (1 of 1).
- Overlay isolation: post-unmount, pre-edit response returns (1 of 1).
- No covariance NaN or divergence during precomputation.
- Edit-success metric within ±5% of the published CounterFact reference
  number for the chosen reference fact.

Partial pass:
- L1 storage probe succeeds and overlay isolation succeeds, but the
  edit-success metric drifts more than ±5% from the published reference.
  This indicates a numerical-precision issue worth diagnosing on Kaggle
  before activating RunPod.

Fail:
- L1 storage probe fails (the edit didn't take).
- Overlay non-isolation (the edit persists after unmount).
- Covariance NaN or divergence.
- Environment doesn't support MEMIT (PyTorch / CUDA version mismatch
  that cannot be resolved within Kaggle).

A FAIL halts the session. Diagnose before activating RunPod.
</smoke_test_specification>

<method>
Work through the three blocks in order. Block 2 is gated on Block 1
passing.

# Block 1 — Kaggle Smoke Test (free, ~1-3 days operator time)

1. Verify Kaggle account state. Walk the operator through:
   - Account creation if needed.
   - Phone verification (gates GPU access).
   - Notebook quota status (GPU hours remaining this week).

2. Verify current state of MEMIT reference repository via web_fetch:
   - github.com/kmeng01/memit — current default branch, recent commits,
     any open issues that might affect smoke test reproducibility.
   - hparams/MEMIT/EleutherAI_gpt-j-6B.json — confirm hyperparameter file
     is intact and current.
   - Identify a specific commit SHA to pin for the smoke test (do not
     use HEAD; pin to a specific SHA the operator can record).

3. Verify GPT-J 6B HuggingFace state via web_fetch:
   - huggingface.co/EleutherAI/gpt-j-6b — current model file SHA, last
     update, any known integrity flags.
   - Pin the specific revision SHA.

4. Walk the operator through Kaggle notebook setup:
   - Create new notebook with GPU enabled (P100 16 GB or 2× T4 32 GB).
   - First cell: pin Python package versions (torch, transformers,
     accelerate). Use the versions MEMIT's reference notebook expects.
   - Second cell: clone MEMIT at the pinned SHA.
   - Third cell: download GPT-J 6B at the pinned revision; convert to
     FP16; verify checkpoint SHA matches expected.

5. Walk the operator through the smoke test execution:
   - Run MEMIT covariance precomputation on a single target layer
     (suggested: layer 17 of 28, mid-band per the model's layer count).
   - Save covariance matrix; verify no NaN.
   - Select one CounterFact reference fact from the published paper
     (Claude should suggest a specific fact citation from the original
     MEMIT paper or kmeng01/memit's evaluation suite).
   - Run MEMIT edit on this single fact.
   - Run L1 storage probe (read-back) to verify the edit took.
   - Save the edited overlay; unmount; re-run the elicitation prompt;
     verify pre-edit response returns (overlay isolation check).
   - Compare edit-success metric to the published reference; note
     any drift.

6. Record the verdict per the smoke test specification above.

7. If verdict is FAIL or ambiguous-PARTIAL: HALT the session.
   Diagnose before any RunPod activation. The session can re-open
   once the issue is identified.

# Block 2 — RunPod Activation (gated on Block 1 PASS)

Only proceed if Block 1 returned PASS or clean PARTIAL.

1. Walk the operator through RunPod account creation:
   - Account signup; identity verification if required.
   - Payment method addition (operator-provided; Claude does not see
     payment data).
   - Billing alert configuration (suggested: alert at $50, $150, $300
     monthly to track POC burn rate).

2. Provision the Network Volume:
   - 100 GB initial allocation in the same region as the intended
     GPU pod. Confirm region selection BEFORE provisioning — Network
     Volumes cannot be cross-region attached.
   - Verify Network Volume is mounted and writable from a test pod.

3. Walk the operator through pinned PyTorch container image selection:
   - List available PyTorch images on RunPod's catalog.
   - Identify the image whose torch version matches what the Kaggle
     smoke test used. Do NOT use a "latest" tag — pin by digest.
   - Record the image digest in the reproducibility manifest.

4. Run a dry-run pod:
   - Spin up an RTX 4090 pod with the pinned image and the Network
     Volume mounted.
   - Verify the same MEMIT reference repository checkout works in
     this environment.
   - Run the same single-fact MEMIT edit from the smoke test on the
     RunPod pod (this exercises HC-2 in the production environment).
   - Verify the edit-success metric matches the Kaggle result within
     reasonable noise. Material drift between Kaggle and RunPod is a
     signal that the environments differ in ways that affect MEMIT's
     numerical behavior — surface this as a diagnostic for the operator.
   - Tear down the pod (the Network Volume persists).

# Block 3 — Persistent State Architecture and Reproducibility Manifest

1. Define the Network Volume directory layout. Suggested:
   ```
   /workspace/
     architecture_profile/        # PF-1..PF-6 outputs at Stage 1
     vindex_overlays/              # MEMIT edit overlays per stage
     cfb_baseline/                 # CFB v1 corpus + pre-edit baseline (Stage 0)
     covariance_caches/            # PF-5 covariance matrices, content-hashed
     drift_sweep_results/          # Stage 2 outputs
     epsilon_calibration/          # Stage 3a outputs
     compaction_probe_calibration/ # Stage 3b outputs
     judge_calibration/            # Stage 3c outputs
     reproducibility_manifest.json # the pinned-version record
     session_logs/                 # per-session execution logs
   ```
   Confirm or adjust with the operator.

2. Configure local rsync target on the 2020 MBP:
   - Identify a local directory the rsync will mirror to.
   - Confirm available disk space (rough estimate: 100 GB to be safe;
     covariance caches are the largest category).
   - Walk through rsync command syntax for weekly mirror.
   - Note: rsync target is a backup, not the source of truth. Network
     Volume on RunPod is the source of truth during the POC.

3. Compose the reproducibility manifest:
   ```json
   {
     "manifest_version": "1.0",
     "kaggle_smoke_test": {
       "verdict": "PASS|PARTIAL|FAIL",
       "completed_at": "<timestamp>",
       "memit_repo_sha": "<pinned SHA>",
       "gpt_j_revision_sha": "<HF revision>",
       "tokenizer_sha": "<tokenizer.json SHA>",
       "torch_version": "<exact version>",
       "transformers_version": "<exact version>",
       "edit_success_metric": "<measured>",
       "published_reference": "<cited>",
       "drift_from_reference": "<value>"
     },
     "runpod_dry_run": {
       "pod_image_digest": "<image digest>",
       "completed_at": "<timestamp>",
       "edit_success_metric": "<measured>",
       "drift_from_kaggle": "<value>"
     },
     "persistent_state": {
       "network_volume_id": "<id>",
       "network_volume_region": "<region>",
       "network_volume_size_gb": 100,
       "directory_layout_committed": true
     },
     "rsync_target": {
       "local_path": "<path on MBP>",
       "cadence": "weekly"
     }
   }
   ```
   This manifest is the seed for `architecture_profile.json` (PF-6).
   Save it to the Network Volume root.

4. Record final account and infrastructure state in the Session
   Summary Block.
</method>

<output_format>
Produce a single markdown document with these sections, in order:

## Bottom Line
Two-sentence summary: smoke test verdict; whether RunPod was activated;
state of persistent storage. If session halted, name the halt reason.

## Block 1 — Kaggle Smoke Test Record
Step-by-step record of what was done, what was observed, the verdict,
and any deviations from the planned protocol.

## Block 2 — RunPod Activation Record (if Block 1 passed)
Account state, Network Volume state, dry-run pod outcome, any
operational notes (capacity availability, container image issues,
billing-alert confirmation).

## Block 3 — Persistent State and Reproducibility Manifest
Final directory layout on Network Volume; rsync target configuration;
the full reproducibility manifest as JSON.

## Open Questions / Carry-Forward to Stage 1
Anything observed during the smoke test or dry-run that informs Stage 1
planning. Examples: GPU memory headroom observation; covariance
precomputation timing; container image version notes.

## Halt Notice (only if session halted)
What was attempted; where it failed; what to diagnose; what next
session should re-open.

## Session Summary Block
Standard format. Decisions made / Constraints established / Open
questions deferred / Interface contracts defined (if any) /
Next session candidates.
</output_format>

<constraints>
- Do NOT execute commands on behalf of the operator. Claude is the
  navigator. The operator runs the commands on their own machine,
  Kaggle account, and RunPod account.
- Do NOT have the operator paste API keys, payment information, or
  account credentials into the chat. Claude does not need to see them
  to navigate the session.
- Do NOT skip the smoke test. It is the load-bearing checkpoint
  before paid activation. Even if the operator wants to "just go to
  RunPod directly," the smoke test discipline was confirmed in the
  prior session and should not be relaxed.
- Do NOT default to "latest" tags or HEAD branches when pinning
  versions. Every pinned version is a specific SHA or digest. The
  reproducibility manifest depends on this discipline.
- Do NOT begin full Stage 1 SECT (three counterfactual facts × three
  runs each). The smoke test is one fact, one run. Stage 1 is its
  own session with its own GPU-hour budget.
- Do NOT begin probe-set v1 or CFB v1 authorship in this session.
  Those are separate Stage 0 sub-sessions with `validation-contract-
  architect` primary skill.
- If a verification step surfaces a toolchain incompatibility (e.g.,
  current MEMIT repo HEAD doesn't run on a current PyTorch wheel),
  do not work around it silently. Pin to an older commit if needed,
  record the pinning decision, surface the regression as an open
  question for the operator.
</constraints>

<stopping_rule>
The session is complete when ONE of the following holds:

1. **Successful path:** Kaggle smoke test passes; RunPod activated;
   Network Volume provisioned; reproducibility manifest recorded;
   Session Summary Block produced.

2. **Halt path:** Kaggle smoke test fails or surfaces a toolchain
   issue; RunPod NOT activated; halt notice recorded; Session Summary
   Block produced with the halt reason and the diagnosis next-step.

The session does NOT proceed to Stage 1 SECT execution, full
architecture_profile.json drafting, CFB v1 authorship, or probe-set v1
authorship. Each of those is its own session.
</stopping_rule>
```

---

*End of session prompt.*
