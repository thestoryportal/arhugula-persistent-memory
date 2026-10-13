# Stage 1 SECT Runbook — meta-llama/Llama-3.1-8B

> **Authoring session:** S2.5a-runbook (dedicated)
> **Predecessor session:** Session 2.5a (CLOSED PARTIAL with smoke test PASS)
> **Consumer session:** Stage 1 SECT re-attempt session (post-S2.7 / post-P-7 NV-application)
> **Target environment:** RunPod RTX 4090 24 GB single GPU; NV `large_amethyst_wolverine`
> **Target model:** `meta-llama/Llama-3.1-8B` (base; not Instruct)
> **Trial protocol:** IC-S24-4 — 5 facts × 3 replicates = 15 trials (S2.12-A; was 3 × 3 = 9 at v1)
> **Inherited cell pattern:** Block 2 RunPod canonical notebook (extended from 10 to 13 cells: Cells 0–12)
> **Specialists:** framework-spec-writer (primary); validation-contract-architect (Cells 6, 7, 9, 10); state-consistency-theorist (Cells 11, 12); memit-specialist (Cells 2–5)
>
> **Revision:** v1.4 — Session 2.9 hardening pass (2026-05-01). Builds on v1.3 (architectural axis EMPIRICALLY-RATIFIED at S2.8; structural axis FULLY-RATIFIED; textual axis DEFECTIVE-IN-FIELD via OQ-S28-3). Closes OQ-S28-2 (Cell 1 fingerprint session label hardcode), OQ-S28-3 (Cell 2 line 552 `hidden_size` defense-in-depth defect — DELETION), OQ-S28-4 (cache vs model SHA equality not gated — Cell 5 stages `model_revision_sha` to env_fingerprint; Cell 11 asserts equality), OQ-S28-7 (HF cache v4.22 migration hygiene — new §0.7 operator-side post-verification step). Codifies D-S28-2 (R1.3 cache-dispatch smoke-load as the canonical C-S26-3 execution-dry-run gate) at new §1.5.1 below. Inherits the S2.8 architectural-axis empirical anchor under the Empirical-Anchor-Inheritance gate (§1.5 v1.4 ratification posture): no v1.4 edit modifies Cells 3, 5, 9 cache-dispatch surface semantics; the S2.8 9/9 cache-dispatch PASS + 9/9 unmount |drift|=0.00 record carries forward unmodified. v1.4 ships under PROVISIONAL status until Stage 1 SECT v2 execution against post-v1.4 NV state ratifies the textual axis; cache-dispatch architectural axis is NOT subject to re-ratification absent a cache-dispatch surface change. C-S28-1 codification (process constraint: hardening passes that authorize defense-in-depth markers must verify post-application source form against fully-patched NV state) is RATIFIED at S2.9 in `memit-patches-canonical.md v2.5 §10.4` (separate amendment artifact). Predecessor v1.3 — Session 2.7 hardening pass (2026-05-01). Absorbs 12 v1.3-routed OQs surfaced at S2.6 first-execution: OQ-S26-2 (Cell 0 HF env-var injection block), OQ-S26-3 (Cell 0-VERIFY library-constant freeze assertion), OQ-S26-5 (Cell 1 skopeo flag version-tolerance), OQ-S26-8 (Cell 2 `compute_z.py` path correction), OQ-S25b-1 (Cell 2 P-4 marker correction `hidden_size` → `max_position_embeddings` count), OQ-S26-9 (process: dry-run gate discipline — codified in §1.5 below), OQ-S26-10 (Cell 0 GPU-memory baseline check), OQ-S26-11 (Cell 0 Jupyter kernel-cleanup procedure documentation), OQ-S26-12 (Cell 5 named-variable model-load split for OOM hygiene), OQ-S26-13 (Cell 5 pad_token anchor inversion), OQ-S26-15 (Cell 7 probe count comment correction), OQ-S26-17 (Cell 3 smoke-load test for cache-dispatch round-trip). New Cell 2 verification logic for P-5, P-6, P-7 markers (P-5 + P-6 were implicit-verified-only at v1.2; P-7 is new at S2.7 per `memit-patches-canonical.md` v2.4 §3.8). C-S26-3 dry-run gate methodology codified in §1.5; this v1.3 is itself authored under provisional-dry-run-pending status (see §1.5 OQ-S27-1 deferral). Predecessor v1.2 — pre-Session-2.6 hardening pass (2026-05-01) — surgical Cell 3 edits closing OQ-PreS26-26 + OQ-PreS26-31 canonically: (a) Cell 3 R1.1 file-set predicate updated to include `_t100_` segment in the expected filename pattern, reconciling against the post-P-6 cache filename interface IC-PreS26-2 (canonical replacement form authored in `memit-patches-canonical.md` v2.3 §3.7); (b) Cell 3 internals consumer added — new R1.2 phase that opens each .npz file and resolves the covariance matrix via the `["mom2.mom2", "mom2", non-metadata-fallback]` priority list per IC-PreS26-3 (MEMIT `runningstats.SecondMoment` reflection convention). Empirical anchor for both edits: pre-S2.6 fork-work re-attempt session Cell 5 PASS verdict 2026-05-01T06:06:17Z (per `pre_s2_6_fork_work_summary_block.md` v2 D-PreS26-7, D-PreS26-8). Predecessor v1.1 — post-review hardening pass. Absorbed reviewer P1 items (R1.1 Cell 3 named-file inventory; R1.2 Cell 9 memory hygiene; R1.3 Cell 9 peak-memory forensics; R1.4 Cell 1 digest drift soft check), high-value P2 items (R2.1 Cell 8 C-S24-7 hard gate; R2.2 Cells 6–7 provenance comments; R2.3 Part XI OQ-S25-1 closure; R2.4 §2.3 NV overlay cost line; R2.5 §9.3 forensic handoff to S2.7), and C3.4 (§10.3 operator post-session checklist). P3 items C3.1–C3.3, C3.5 require no changes per reviewer assessment.

---

## 1.5 Authoring discipline — C-S26-3 dry-run gate

This v1.4 hardening pass is authored under the C-S26-3 dry-run gate constraint (ratified at S2.7 per `memit-patches-canonical.md` v2.4 §10.1):

> **C-S26-3.** Runbook hardening passes must include a dry-run execution against known-good NV state as part of the authoring acceptance gate. A hardening pass that does not exercise its target cells against fully-patched live state cannot be ratified.

**v1.4 dry-run status: AUTHORING-ACCEPTANCE-PENDING.** This v1.4 is authored at S2.9 from S2.8 forensic findings under the four ratification gates enumerated in the S2.9 kickoff prompt §1.3:

| Gate | Trigger | v1.4 disposition at S2.9 close |
|---|---|---|
| Authoring acceptance | All Phase 1 OQs closed in v1.4 source; cell-level diff is reviewable; D-S28-2 codified at §1.5.1 | PROVISIONAL ratification at S2.9 close (no execution dry-run in this session) |
| C-S28-1 application | New defense-in-depth marker added to v1.4 | NOT TRIGGERED — v1.4 contains zero NEW markers; OQ-S28-3 closure is DELETION of the v1.3 line 552 marker |
| Cache-dispatch semantics preservation | v1.4 change to Cells 2, 3, 5, 9 cache-dispatch surfaces | NOT TRIGGERED — Cell 5 OQ-S28-4 edit stages `model_revision_sha` to env_fingerprint (manifest-discipline addition); does not touch cache-dispatch semantics. Cells 3, 9 unchanged. |
| Empirical anchor inheritance | v1.4 change does not affect cache-dispatch semantics | TRIGGERED — v1.4 inherits the S2.8 architectural-axis empirical anchor (9/9 cache-dispatch PASS + 9/9 unmount |drift|=0.00 + R1.3 PASS in 2.72s) without re-execution. |

The full ratification gate (Stage 1 SECT v2 execution against post-v1.4 NV state) is NOT IN S2.9 SCOPE. v1.4 ships under PROVISIONAL status until that future execution session.

If a future session establishes that any v1.4 cell change does affect cache-dispatch semantics (currently not the case per the gate matrix above), the cache-dispatch architectural axis must be re-ratified before v1.4 advances beyond PROVISIONAL — the S2.8 empirical anchor would not carry forward.

### 1.5.1 R1.3 codification — canonical C-S26-3 execution-dry-run gate (D-S28-2)

D-S28-2 (ratified at S2.8 close): R1.3 cache-dispatch smoke-load (Cell 3 §3.8 invocation of `get_cov` on a single edit-layer with `_ConfigOnlyPlaceholder`) is codified as the canonical C-S26-3 execution-dry-run gate for runbook hardening passes targeting cache-dispatch surfaces.

> **Closure of OQ-S27-1.** Dry-run gate scope for runbooks targeting expensive execution cells (Cell 9 trial loop ~30+ min wall-time) is empirically resolved: the lightweight R1.3 smoke-equivalent is sufficient for cache-dispatch defect class detection.

**Empirical anchor (S2.8 close):**

| Surface | R1.3 (lightweight) | Full Cell 9 trial loop |
|---|---|---|
| Cache-dispatch defect detection | PASS in 2.72s on cold start; canonical `Loading cached covariance for layer 4 …` log line | PASS at ~15s/trial (warm) and 32.4s (Trial 0 cold) for 9 trials |
| Architectural-defect-class equivalence | Confirmed at S2.8 — R1.3 PASS preceded full Cell 9 9/9 PASS without divergence | Reference upper bound; load-bearing for full trial verdict but redundant for cache-dispatch detection |
| Cost ratio | 1 | ~1100–1500 |

**Operational binding for hardening passes:**

| Hardening pass scope | Required dry-run gate |
|---|---|
| Modifies cell semantics outside Cells 3, 5, 9 (no cache-dispatch surface touched) | Structural dry-run (Cells 0–8 first-execution PASS without bridge fix) — R1.3 NOT REQUIRED |
| Modifies any cache-dispatch surface (Cell 3 R1.1/R1.2/R1.3, Cell 5 model load, Cell 9 trial loop, OR a patch that affects `get_cov` / `layer_stats` resolution) | R1.3 execution against post-patch NV state — REQUIRED before authoring-acceptance ratification |
| Modifies the full trial protocol (Cell 9 trial loop body, IC-S24-4 protocol changes) | Full Cell 9 Trial 0 dry-run — REQUIRED (R1.3 alone is insufficient for trial-protocol-class defects) |

R1.3 is not a substitute for the full Cell 9 trial loop in cases where the hardening pass changes trial protocol semantics. Its scope is bounded to cache-dispatch defect class detection — the empirically-validated scope at S2.8.

**Cross-reference.** `memit-patches-canonical.md` v2.4 §10.1 (C-S26-3 spec); v2.5 §10.4 (C-S28-1, the marker-correctness companion process constraint).

---

# Part I — Session orientation

## 1.1 Purpose

This runbook drives Session 2.6 — the first Stage 1 SECT (Semantic Edit Coverage Test) execution against the Workstream 1 production target model `meta-llama/Llama-3.1-8B`. It executes the 9-trial matrix defined by IC-S24-4, captures per-trial verdicts against the four Stage 1 acceptance criteria, and emits an aggregate Stage 1 PASS/FAIL verdict.

Stage 1 SECT is the load-bearing empirical step that validates whether MEMIT edits applied to a 2026-vintage 8B-parameter LLaMA model satisfy the `.vindex` overlay isolation properties demonstrated by HC-2 on GPT-J 6B in Session 2.3. Stage 1 PASS gates Workstream 1 progression to Stage 2 sweep design.

## 1.2 Measures

Per IC-S24-4 trial protocol, each of the 9 trials produces a verdict against four criteria:

| Criterion | Definition | Acceptance band | Provenance |
|---|---|---|---|
| **Consistency** | Post-edit top-1 token equals `target_new` and `P(target_new)` exceeds 0.5 | `p_target_new_post > 0.5` | Provisional (D-S24-10; OQ-PROBE-2) |
| **Generalization** | Pre-edit→post-edit drift in top-1 probability for related-but-unedited probes is small | `abs(p_top_1_post − p_top_1_pre) < 0.05` per probe | Provisional |
| **Specificity** (shared, post-edit + post-unmount) | Pre-edit→post-edit and pre-edit→post-unmount drift in top-1 probability for unrelated-domain probes is small | `abs(p_top_1 − p_top_1_pre) < 0.05` per probe per phase | Provisional |
| **Unmount** | Pre-edit→post-unmount drift in `P(target_true)` for the per-fact unmount probe is at the FP16 noise floor | `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4` | **Hard, IC-S23-4 (NOT provisional)** |

Aggregate Stage 1 verdict (Cell 10):

| Aggregate criterion | Threshold | Source |
|---|---|---|
| Consistency aggregate | ≥3 of 5 facts at ≥2 of 3 trials each (per-fact aggregation per OQ-S212A-2) | Provisional |
| Generalization aggregate | ≥3 of 5 facts at ≥2 of 3 trials each | Provisional |
| Shared-specificity aggregate | ≥3 of 5 facts at ≥2 of 3 trials each (for each of post-edit and post-unmount phases) | Provisional |
| Unmount aggregate | **15 of 15 trials PASS** (hard; trial-level invariant under per-fact / ratio choice) | IC-S23-4 |

Stage 1 PASS = all four aggregates PASS. **S2.12-A AMENDMENT (2026-05-03):** Aggregation logic switched from v1's ratio (≥ 8/9) to per-fact (≥3 of 5 facts at ≥2/3 trials each) per OQ-S212A-2 operator decision; unmount remains trial-level invariant.

## 1.3 Inputs

| Artifact | Provenance | Used by |
|---|---|---|
| `cfb-v2.yaml` v0.1 (locks at S2.12-A Cell 7 → v1.0) | S2.12-A authoring | Cells 6, 8 (fact metadata; subject token IDs) |
| `probe-set-v2.yaml` v0.1 (locks at S2.12-A Cell 7 → v1.0) | S2.12-A authoring | Cells 7, 8, 9 (probe prompts + acceptance bands) |
| `meta-llama_Llama-3.1-8B.json` (20-field schema) | Session 2.5a | Cell 4 (hparams) |
| `stage_1_sect_overlay/` (NV) | freshly produced per trial | Cell 9 (per-trial overlay snapshots) |
| Fresh covariance cache at `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` | **pre-S2.6 fork-work session** (NOT this session) | Cells 3, 9 (consumed by `apply_memit_to_model`) |
| `PROVENANCE.txt` colocated with cache | pre-S2.6 fork-work session | Cell 3 (gating predicate) |
| MEMIT repo at `/workspace/memit_dry_run/memit/` (P-1, P-2, P-4 applied) | Sessions 2.3 + 2.5a | Cells 2, 9 |
| Llama-3.1-8B base in `/workspace/hf_cache/` | Session 2.5a | Cell 5 |

## 1.4 Outputs

| Artifact | Path | Producer | Consumer |
|---|---|---|---|
| `stage_1_llama_baselines.json` | `/workspace/architecture_profile/stage_1_llama_baselines.json` | Cell 7 | Cells 9, 10; Session 2.7 retrospective |
| `stage_1_trial_<fact_id>_r<replicate>.json` (×15 at v2: 5 facts × 3 replicates) | `/workspace/stage_1_sect/trials/` | Cell 9 (per trial) | Cell 10; Session 2.13 |
| `stage_1_sect_overlay/<fact_id>/r<replicate>/` (×15 at v2) | `/workspace/stage_1_sect/overlays/` | Cell 9 (per trial) | Session 2.13 forensics |
| `stage_1_aggregate_verdict.json` | `/workspace/stage_1_sect/aggregate_verdict.json` | Cell 10 | Session 2.7 (gating); reproducibility manifest |
| Updated `reproducibility_manifest.json` | `/workspace/reproducibility_manifest.json` | Cell 12 | Session 2.7+ |
| SSD mirror sync trigger log | `/workspace/stage_1_sect/mirror_sync.log` | Cell 12 | operator forensics |

## 1.5 Stage 1 PASS criteria (load-bearing)

```
STAGE_1_PASS = (                                  # S2.12-A: per-fact aggregation per OQ-S212A-2
    consistency_aggregate_pass     # ≥3 of 5 facts at ≥2/3 trials each w/ consistency probes PASS (p_target_new_post > 0.5)
    AND generalization_aggregate_pass     # ≥3 of 5 facts at ≥2/3 trials each w/ gen probes PASS (drift_p_top_1 < 0.05)
    AND specificity_post_edit_aggregate_pass     # ≥3 of 5 facts at ≥2/3 trials each w/ 3 shared-spec drift < 0.05 post-edit
    AND specificity_post_unmount_aggregate_pass  # ≥3 of 5 facts at ≥2/3 trials each w/ 3 shared-spec drift < 0.05 post-unmount
    AND unmount_aggregate_pass            # 15/15 trials w/ unmount probe drift < 1e-4 (HARD per IC-S23-4; trial-level)
)
```

The unmount aggregate is the only hard-gated criterion. The other three are provisional pending OQ-PROBE-2 calibration at Session 2.7.

## 1.6 Halt-path summary (full taxonomy in Part IX)

| Halt class | Scope | Recovery path |
|---|---|---|
| **Pre-flight failure** (Cells 0–2) | Session-level | Resolve dep / patch state; restart kernel; resume from Cell 0 |
| **Cache provenance failure** (Cell 3) | Session-level | **Hard halt.** Session 2.6 cannot proceed. Schedule pre-S2.6 fork-work session if not yet executed |
| **Hparams / model load failure** (Cells 4–5) | Session-level | Investigate; likely OQ-S25-3 or OQ-S25-4 territory |
| **Tokenizer single-token failure** (Cell 6) | Session-level | Halt; revise affected fact in cfb-v1; re-version corpus; defer to S2.7 |
| **Pre-edit baseline anomaly** (Cell 7) | Session-level | Investigate divergence from S2.5a smoke test; possible OQ-S25-10 escalation |
| **Trial-level criterion failure** (Cell 9) | Trial-level | **Continue.** Per-fact aggregation (S2.12-A) tolerates up to 1 trial failure per fact at the ≥2/3 per-fact threshold AND up to 2 catastrophic-failure facts at the ≥3/5 facts threshold |
| **Trial-level unmount-band failure** (Cell 9) | **Session-level (immediate halt)** | State is contaminated. Stop session. Forensics over post-unmount overlay snapshot |
| **Inter-trial baseline-drift gate failure** (Cell 9) | **Session-level (immediate halt)** | State accumulated drift across trials. Stop. Investigate Copy-Unmount fidelity |
| **NV write / manifest failure** (Cells 11–12) | Recoverable | Re-run with verified inputs; do not re-run trial loop |

---

# Part II — Pod configuration

## 2.1 Hardware target

| Setting | Value | Rationale |
|---|---|---|
| GPU | 1× RTX 4090 24 GB (Secure Cloud) | Stage 1 production target per Session 2.1; matches S2.5a smoke test environment; FP64 GPU solve fits in envelope (no P-3') |
| Pod type | On-demand | Session 2.1 venue lock |
| Region priority | US-NC-1 (NV-pinned) | NV `large_amethyst_wolverine` is region-pinned to US-NC-1 (per S2.5a closure note); cannot be relocated without NV destruction |
| Container image | `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` | Digest `sha256:61a4aafb...`; image tag is informational, digest is canonical (C-S25-2-class; Block 2 Delta D1) |
| Network Volume | `large_amethyst_wolverine` (`nvol-s1xi9zhfc2`); mount at `/workspace` | Inherited from S2.5a; ~33 GB occupied at session start |
| Working directory | `/workspace/memit_dry_run/memit/` for any MEMIT-importing cell | C-S25-5 (MEMIT cwd invariant) |

## 2.2 Pre-existing NV state (verified at Cell 2 / Cell 3 / Cell 5)

| Path | Contents | Cell that verifies |
|---|---|---|
| `/workspace/memit_dry_run/memit/` | MEMIT repo with P-1, P-2, P-4 applied | Cell 2 |
| `/workspace/hf_cache/` | Llama-3.1-8B base (~16 GB; HF_HOME-redirected per D-S25-8) | Cell 5 |
| `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` | **Fresh** cache produced by pre-S2.6 fork-work session; bridge cache from S2.5a has been REPLACED | Cell 3 |
| `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/PROVENANCE.txt` | Structured provenance assertion | Cell 3 (hard gate) |
| `/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json` | Corrected 20-field hparams schema | Cell 4 |

## 2.3 Cost projection

| Phase | Wall time | GPU cost | NV cost |
|---|---|---|---|
| Pre-flight (Cells 0–6) | ~15–20 min | ~$0.20 | — |
| Pre-edit baseline capture (Cell 7) | ~3–5 min | ~$0.05 | — |
| Trial loop (Cells 8–10), 9 trials × ~5–7 min | ~50–70 min | ~$0.80–1.10 | — |
| Persistence + manifest (Cells 11–12) | ~5–10 min | ~$0.10 | ~$0.05 |
| **Total** | **~75–105 min** | **~$1.15–1.45** | **~$0.05** |

**Trial overlay snapshot NV usage:** ~1.6 GB additional NV allocation (9 trials × ~180 MB each, `edited.pt` + `original.pt` per trial). Total NV at session end: ~35 GB (vs ~33 GB at session start).

Within OQ-S25-2 envelope. If session exceeds 2 hours wall time, halt and investigate.

## 2.4 Operator-side preconditions (before Cell 0)

- [ ] Pre-S2.6 fork-work session completed; PROVENANCE.txt asserted at canonical cache path
- [ ] Pod started against NV `large_amethyst_wolverine`; image digest reconciled
- [ ] `lonely_moccasin_mandrill` or replacement pod healthy; `/workspace` mounted at ~33 GB pre-state
- [ ] HF token persisted in `~/.cache/huggingface/token` (gated-public-repo permission; C-S25-4)
- [ ] Billing alerts configured (≥ $50 per S2.1; ≥ $5 within-session sentinel for this run)

---

# Part III — Pre-flight (Cells 0–2)

## Cell 0 — System binaries + Python deps

**Specialist:** framework-spec-writer (runbook discipline) + memit-specialist (MEMIT dep manifest)

**Purpose:** Re-establish the full Block 2 §12 dependency manifest plus the C-S25-7 pandas-runtime extension on a fresh container. Container-disk Python state is non-persistent across pod stop/start (C-S25-2); this cell is mandatory on every session start.

**Inputs:** Fresh container; NV mounted at `/workspace`.

### 0.1 Pre-launch GPU baseline (operator-side; before launching Jupyter)

Per OQ-S26-10 (closed at v1.3): the predecessor-session orphan-kernel risk surfaces as Cell 5 model-load OOM. Verify GPU clean state before launching Jupyter:

```bash
# Run in pod terminal BEFORE launching Jupyter
nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits
# Expected: integer < 1024 (i.e., < 1 GiB used)
# If > 1 GiB: identify and clear orphan compute apps
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader
# For each non-current orphan: kill -SIGTERM <pid> ; verify with nvidia-smi
```

If GPU memory.used ≥ 1 GiB at session start, halt before Cell 0 and reconcile. Acceptable causes: kernel restart cleared but driver-side alloc tracking is stale (re-check after 30 sec); intentional persistent compute app (document and proceed).

### 0.2 Jupyter kernel hygiene (informational; OQ-S26-11)

Jupyter `MappingKernelManager` auto-restarts ipykernels killed via OS-level SIGTERM/SIGKILL with original kernel UUIDs. Permanent termination requires Jupyter API or UI-side action. If a session-start GPU baseline shows orphan compute-app contention from a prior Jupyter session:

| Path | Mechanism | When to use |
|---|---|---|
| Pod stop / start | Driver-level state reset; all kernels and compute apps cleared | Default; works always; ~10–25 min GPU re-acquisition latency |
| Jupyter UI "Shut Down Kernel" | Permanent kernel termination via Jupyter API | Pod is running, Jupyter accessible; preferred for in-place hygiene |
| `DELETE /api/kernels/{kernel_id}` via curl | API-level termination | Pod is running, Jupyter accessible, batch cleanup |
| Shell `kill -SIGTERM <pid>` | OS-level kill; **autorestart fires** unless Jupyter UI/API also called | Last-resort; understand autorestart implication |

For S2.6-style in-session orphan-kernel discovery, the canonical recovery is current-kernel restart (Path B per D-S26-6) plus pod-terminal `kill -SIGTERM` of the identified orphan PID.

### 0.3 System binaries

```bash
# Run in pod terminal BEFORE launching Jupyter
# Working directory: /workspace
# === System binaries ===
apt-get update -qq
apt-get install -y --no-install-recommends rsync skopeo

# Verify
which rsync && rsync --version | head -1
which skopeo && skopeo --version
```

### 0.4 HuggingFace cache env-var injection block (OQ-S26-2; D-PreS26-10 codified)

Per OQ-S26-2 (closed at v1.3): D-PreS26-10's six-var HF cache discipline must be applied via `os.environ` injection inside the Cell 0 Jupyter kernel BEFORE any HF-stack import. Shell-level exports do not propagate to a Jupyter kernel started by a server that pre-dates the exports (D-S26-2 empirical anchor).

Run this block as the **first Python cell** after Jupyter launch, before Cell 0 dep-install:

```python
# === CELL 0 PRE-INJECT — HF cache env-var freeze (D-PreS26-10) ===
# Run BEFORE any transformers / datasets / huggingface_hub import.
# References: D-PreS26-10 (six-var discipline); OQ-S26-2 (v1.3 closure).

import os
os.environ["HF_HOME"]            = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"]       = "/workspace/hf_cache/hub"
os.environ["HF_DATASETS_CACHE"]  = "/workspace/hf_cache/datasets"
os.environ["HF_ASSETS_CACHE"]    = "/workspace/hf_cache/assets"
os.environ["HF_HUB_OFFLINE"]     = "0"
# TRANSFORMERS_CACHE retained for transformers < 5.0 compatibility;
# deprecated at transformers 5.0 — see OQ-S26-4 for forward-compatibility note
os.environ["TRANSFORMERS_CACHE"] = "/workspace/hf_cache"

print("Cell 0 PRE-INJECT: six HF env vars set in os.environ (D-PreS26-10).")
print("Proceeding to Cell 0 dep install.")
```

### 0.5 Dep-install

```python
# === CELL 0 — Block 2 §12 dep manifest + pandas runtime extension ===
# Specialist: framework-spec-writer + memit-specialist
# References: C-S25-6, C-S25-7; OQ-S23-4 iteration 3; block-2-3-runbook-deltas §12

import subprocess, sys

PY = sys.executable

# Phase 1: Load-bearing + import-time-only + hydra chain (single bulk install)
subprocess.run([PY, "-m", "pip", "install", "--quiet",
    "transformers==4.45.2",
    "accelerate==0.34.2",
    "huggingface_hub==0.25.2",
    "tokenizers==0.20.3",
    "safetensors==0.4.5",
    "datasets==4.8.3",
    "matplotlib==3.9.2",
    "scipy==1.14.1",
    "scikit-learn==1.5.2",
    "hydra-core==1.3.2",
    "einops==0.7.0",
    "nltk==3.8.1",
], check=True)

# Phase 2: pandas force-reinstall (--no-deps to avoid blowing away the loadout above)
subprocess.run([PY, "-m", "pip", "install", "--quiet",
    "--force-reinstall", "--no-deps", "pandas==2.2.3",
], check=True)

# Phase 3: pandas runtime deps not covered by --no-deps (C-S25-7)
subprocess.run([PY, "-m", "pip", "install", "--quiet",
    "pytz", "tzdata",
], check=True)

print("Cell 0 install complete. RESTART KERNEL NOW (mandatory per OQ-S23-4 iter 3).")
print("After restart, re-run Cell 0 PRE-INJECT (§0.4) before any HF-stack import,")
print("then proceed to Cell 0-VERIFY.")
```

**MANDATORY KERNEL RESTART AFTER CELL 0.** Discovery-by-failure is structurally incompatible with C extension caching (OQ-S23-8 taxonomy: C extension version mismatch → restart required). Do not skip.

**v1.3 NOTE.** After kernel restart, the §0.4 PRE-INJECT block must be re-run before any HF-stack import. Kernel restart clears `os.environ` mutations made by the pre-restart kernel; PRE-INJECT must establish the six-var discipline in the post-restart kernel before Cell 0-VERIFY's `import transformers` statement fires.

After restart, run §0.4 PRE-INJECT then this verification block:

```python
# === CELL 0-VERIFY (after kernel restart + PRE-INJECT re-run) ===
import sys
import transformers, accelerate, huggingface_hub, tokenizers, safetensors
import datasets, matplotlib, pandas, scipy, sklearn
import hydra, einops, nltk
import pytz, tzdata, torch

print(f"Python:           {sys.version.split()[0]}")
print(f"torch:            {torch.__version__}")
print(f"transformers:     {transformers.__version__}")
print(f"accelerate:       {accelerate.__version__}")
print(f"datasets:         {datasets.__version__}")
print(f"huggingface_hub:  {huggingface_hub.__version__}")
print(f"tokenizers:       {tokenizers.__version__}")
print(f"safetensors:      {safetensors.__version__}")
print(f"pandas:           {pandas.__version__}")
print(f"matplotlib:       {matplotlib.__version__}")
print(f"scipy:            {scipy.__version__}")
print(f"sklearn:          {sklearn.__version__}")
print(f"hydra-core:       {hydra.__version__}")
print(f"einops:           {einops.__version__}")
print(f"nltk:             {nltk.__version__}")

assert transformers.__version__ == "4.45.2"
assert accelerate.__version__ == "0.34.2"
assert datasets.__version__ == "4.8.3"
assert pandas.__version__ == "2.2.3"

# v1.3 — D-PreS26-10 library-constant freeze assertion (OQ-S26-3 closure)
# Verifies the PRE-INJECT (§0.4) propagated through to huggingface_hub's
# library-internal HF_HUB_CACHE constant — defense-in-depth against any
# HF-stack version that resolves the constant before our os.environ mutation.
import huggingface_hub.constants
assert huggingface_hub.constants.HF_HUB_CACHE == "/workspace/hf_cache/hub", (
    f"D-PreS26-10 violated: huggingface_hub.constants.HF_HUB_CACHE = "
    f"{huggingface_hub.constants.HF_HUB_CACHE!r} (expected /workspace/hf_cache/hub). "
    f"PRE-INJECT block (§0.4) was not executed before HF-stack import. "
    f"RESTART KERNEL, run §0.4 first, then re-run Cell 0-VERIFY."
)
print(f"\nhuggingface_hub.constants.HF_HUB_CACHE = "
      f"{huggingface_hub.constants.HF_HUB_CACHE!r}  (D-PreS26-10 verified)")

print("\nCell 0-VERIFY: PASS")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `transformers.__version__` | `4.45.2` |
| `accelerate.__version__` | `0.34.2` |
| `datasets.__version__` | `4.8.3` |
| `pandas.__version__` | `2.2.3` |
| `pytz`, `tzdata` importable | True |
| `huggingface_hub.constants.HF_HUB_CACHE` | `/workspace/hf_cache/hub` (D-PreS26-10 freeze) |
| Pre-launch GPU memory.used | `< 1024 MiB` (§0.1 baseline) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `pip install` non-zero exit | Pre-flight failure | Investigate; possible network issue; retry once |
| Post-restart `ImportError` for any package | Pre-flight failure | Re-run Cell 0; if persistent, investigate image drift |
| Version mismatch in CELL 0-VERIFY assertions | Pre-flight failure | Manifest discipline violation; halt session |
| `huggingface_hub.constants.HF_HUB_CACHE` mismatch | Pre-flight failure | PRE-INJECT (§0.4) was not executed before HF-stack import; restart kernel and re-run §0.4 first |
| Pre-launch GPU memory.used ≥ 1 GiB without operator-acknowledged cause | Pre-flight failure | Predecessor-session orphan compute app likely; reconcile per §0.2 before proceeding |

### 0.6 Cell 0 operator constants — SESSION_LABEL bind (OQ-S28-2 closure)

**Purpose.** v1.4 parameterizes the Cell 1 fingerprint `session` field via a Cell 0 `SESSION_LABEL` constant. Operator binds this constant before Cell 1 runs.

**Execution.** Run this block in the Jupyter kernel after Cell 0-VERIFY PASSes and before Cell 1:

```python
# === §0.6 — SESSION_LABEL operator-bind (v1.4; OQ-S28-2 closure) ===
# Bind a session-correct identifier for the Cell 1 fingerprint.
# Format convention: "<session number> — <short description>"
SESSION_LABEL = "2.X — Stage 1 SECT execution"  # OPERATOR EDIT THIS LINE

# Defensive log
print(f"SESSION_LABEL = {SESSION_LABEL!r}")
assert SESSION_LABEL.startswith("2.") and "—" in SESSION_LABEL, (
    "SESSION_LABEL convention violated: expected '<2.N> — <description>' form"
)
print("Cell 0 §0.6: SESSION_LABEL bound; ready for Cell 1.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `SESSION_LABEL` set in kernel globals | True |
| Format starts with `2.` and contains an em-dash | True |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `SESSION_LABEL` not set when Cell 1 runs | Manifest discipline | Cell 1 falls back to placeholder string and flags drift; operator should re-run Cell 0 §0.6 with correct value before manifest publication |

**Cross-reference.** OQ-S28-2 (closure); Cell 1 fingerprint emission (§Cell 1 — Environment fingerprint).

### 0.7 HF cache v4.22 migration hygiene (OQ-S28-7 closure; one-time per pod lifecycle)

**Purpose.** transformers v4.22 introduced a new HF cache layout (the `hub/` prefix). At first transformers import on a fresh pod, the library detects any legacy-layout snapshots under `$HF_HOME/models--<org>--<model>/` and copies them into the new layout under `$HF_HOME/hub/models--<org>--<model>/`. The migration emits a `Migrating your old cache` log line at Cell 0-VERIFY's `import transformers` step. The legacy-layout source is NOT deleted by the migration — it persists as a duplicate (~15 GB for Llama-3.1-8B FP16) and contributes to NV pressure across the pod lifecycle. S2.8 surfaced this at NV utilization 92% close; OQ-S28-7 routes the operator-side cleanup convention into v1.4.

**Execution.** Run this block in the pod terminal (NOT in the Jupyter kernel) after Cell 0-VERIFY PASSes and before Cell 1:

```bash
# === §0.7 — HF cache v4.22 migration cleanup (operator-side; OQ-S28-7) ===
# Run AFTER Cell 0-VERIFY PASS; BEFORE Cell 1.
# Trigger: a "Migrating your old cache" line appeared in Cell 0-VERIFY output.
# If that line did NOT appear, the v4.22 migration already happened on a prior
# pod lifecycle or never had legacy state to migrate — skip this step.

# Step 1: confirm post-migration layout intact under hub/ prefix
ls -la /workspace/hf_cache/hub/models--meta-llama--Llama-3.1-8B/snapshots/ 2>/dev/null \
    && echo "PASS: hub/ layout present"

# Step 2: detect legacy-layout duplicate (sibling, NOT under hub/)
LEGACY=/workspace/hf_cache/models--meta-llama--Llama-3.1-8B
if [ -d "$LEGACY" ]; then
    echo "Legacy-layout duplicate detected at: $LEGACY"
    du -sh "$LEGACY"
    # Step 3: inode comparison — verify hub/ copy is independent
    HUB=/workspace/hf_cache/hub/models--meta-llama--Llama-3.1-8B
    LEG_INODE=$(stat -c %i "$LEGACY/snapshots" 2>/dev/null | head -1)
    HUB_INODE=$(stat -c %i "$HUB/snapshots" 2>/dev/null | head -1)
    if [ "$LEG_INODE" != "$HUB_INODE" ] && [ -n "$HUB_INODE" ]; then
        echo "Inodes differ: hub/ is independent of legacy. Safe to delete legacy."
        # Step 4: deletion (operator-confirmed)
        rm -rf "$LEGACY"
        echo "PASS: legacy-layout duplicate deleted; ~15 GB reclaimed"
    else
        echo "WARN: inode comparison inconclusive — investigate before deleting"
    fi
else
    echo "PASS: no legacy-layout duplicate (migration already cleaned, or never present)"
fi

# Step 5: post-cleanup df check
df -BG /workspace
```

**Verification anchors:**

| Anchor | Expected (post-cleanup) |
|---|---|
| `/workspace/hf_cache/hub/models--meta-llama--Llama-3.1-8B/snapshots/` | Exists, contains the model snapshot |
| `/workspace/hf_cache/models--meta-llama--Llama-3.1-8B/` | Does NOT exist (deleted) |
| `/workspace` free space delta | +~15 GB vs. pre-cleanup |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `hub/` layout missing | Pre-flight failure | Cell 5 model load will fail; investigate v4.22 migration completion before proceeding |
| Inode comparison inconclusive | Soft warning | Skip deletion; document in operator log; revisit at session close |

**Cross-reference.** OQ-S28-7 (closure); OQ-S28-6 (NV utilization sustainability — §0.7 contributes ~15 GB reclaim toward Stage 2 entry NV budget).

---

## Cell 1 — Environment fingerprint + image digest reconciliation

**Specialist:** framework-spec-writer + state-consistency-theorist (manifest discipline)

**Purpose:** Capture runtime-observed environment state (NOT tag-implied) into structured form for the reproducibility manifest. Per Block 2 Delta D1 + C1/C2: image patch-level versions drift from the human-readable tag; the digest is canonical.

**Inputs:** Cell 0 + verify complete; pod terminal accessible.

```python
# === CELL 1 — Environment fingerprint + image digest reconciliation ===
# Specialist: framework-spec-writer + state-consistency-theorist
# References: Block 2 Delta D1; C1, C2
# v1.4 OQ-S28-2 closure: SESSION_LABEL parameterized via Cell 0 constant
# (operator-set per consumer session). Successor sessions re-bind SESSION_LABEL
# at Cell 0 to a session-correct value before running Cell 1.

import sys, platform, subprocess, json, torch
from datetime import datetime, timezone

# v1.4: SESSION_LABEL convention — operator binds at Cell 0 prior to Cell 1.
# If unset (rare), defaults to a placeholder that flags drift in the manifest.
SESSION_LABEL = globals().get("SESSION_LABEL", "OPERATOR_TO_FILL — Stage 1 SECT execution")

fingerprint = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session": SESSION_LABEL,
    "python":           sys.version.split()[0],
    "platform":         platform.platform(),
    "torch":            torch.__version__,
    "cuda_torch":       torch.version.cuda,
    "cudnn":            torch.backends.cudnn.version(),
    "gpu_available":    torch.cuda.is_available(),
}

if torch.cuda.is_available():
    fingerprint["gpu_count"] = torch.cuda.device_count()
    gpus = []
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        gpus.append({
            "index": i,
            "name": props.name,
            "total_memory_gb": round(props.total_memory / 1e9, 2),
            "compute_capability": f"sm_{props.major}{props.minor}",
        })
    fingerprint["gpus"] = gpus

# Driver and image identity
nvsmi = subprocess.check_output(
    ["nvidia-smi", "--query-gpu=driver_version,name,memory.total", "--format=csv,noheader"],
    text=True
).strip()
fingerprint["nvidia_smi"] = nvsmi

# Image digest (skopeo-verified per OQ-S23-17; image tag is informational)
# v1.3 NOTE (OQ-S26-5 closure): skopeo --no-tags flag was introduced in skopeo 1.8.0;
# Ubuntu Jammy ships skopeo 1.4.1. The version-tolerant dispatch below uses
# skopeo inspect WITHOUT --no-tags (works on all versions). Image digest is
# identical across both forms; --no-tags only suppresses the tags array in output.
fingerprint["skopeo_version"] = subprocess.check_output(
    ["skopeo", "--version"], text=True
).strip()
# If the operator has an environment variable RUNPOD_IMAGE_DIGEST set, capture it; otherwise document
fingerprint["image_tag_implied"] = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"
import os
fingerprint["image_digest_observed"] = os.environ.get("RUNPOD_IMAGE_DIGEST", "OPERATOR_TO_FILL_VIA_SKOPEO")

# R1.4 — image digest drift soft check (per OQ-S23-2; warns but does not halt)
EXPECTED_DIGEST_PREFIX = "sha256:61a4aafb"
if fingerprint["image_digest_observed"].startswith(EXPECTED_DIGEST_PREFIX):
    fingerprint["image_digest_match"] = "EXPECTED"
elif fingerprint["image_digest_observed"] == "OPERATOR_TO_FILL_VIA_SKOPEO":
    fingerprint["image_digest_match"] = "DEFERRED — operator to populate via skopeo"
else:
    fingerprint["image_digest_match"] = "DRIFT — investigate per OQ-S23-2"
    print(f"  WARN: image digest drift — got {fingerprint['image_digest_observed'][:32]}..., "
          f"expected prefix {EXPECTED_DIGEST_PREFIX}. Continuing; flag in manifest update.")

# /workspace mount verification
df_workspace = subprocess.check_output(["df", "-BG", "/workspace"], text=True).strip().split("\n")
fingerprint["workspace_mount"] = df_workspace[-1]

print(json.dumps(fingerprint, indent=2))

# Stage to NV
import os
os.makedirs("/workspace/architecture_profile", exist_ok=True)
with open("/workspace/architecture_profile/stage_1_environment_fingerprint.json", "w") as f:
    json.dump(fingerprint, f, indent=2)

# Assertions on Stage 1 production target invariants
assert fingerprint["gpu_count"] == 1, "Stage 1 single-GPU invariant violated"
assert fingerprint["gpus"][0]["name"] == "NVIDIA GeForce RTX 4090", \
    f"Stage 1 hardware invariant violated: {fingerprint['gpus'][0]['name']}"
assert fingerprint["gpus"][0]["compute_capability"] == "sm_89", \
    "Stage 1 compute capability invariant violated"
print("\nCell 1: environment fingerprint staged + invariants verified.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `gpu_count` | `1` |
| `gpus[0].name` | `NVIDIA GeForce RTX 4090` |
| `gpus[0].compute_capability` | `sm_89` (Ada Lovelace) |
| `gpus[0].total_memory_gb` | `~24.00` |
| `torch.__version__` | `2.4.1+cu124` (RunPod image; tag claims 2.4.0) |
| `cuda_torch` | `12.4` |
| `image_digest_observed` populated | True (operator-filled or env-var) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| GPU count > 1 | Pre-flight failure | Stage 1 single-GPU invariant violated; halt |
| GPU name not RTX 4090 | Pre-flight failure | Likely capacity-substitution; halt and re-procure |
| `image_digest_observed == "OPERATOR_TO_FILL_VIA_SKOPEO"` at Cell 12 | Manifest discipline | Operator must populate before reproducibility manifest update |

---

## Cell 2 — MEMIT repo + patch state verification

**Specialist:** memit-specialist (P-1/P-2/P-4/P-5/P-6/P-7 idempotent verification)

**Purpose:** Verify that the MEMIT repo on NV carries the canonical SHA pin AND has all required patches applied. Per IC-S25-2: idempotent re-application is safe; verification is grep-based on patched-file marker substrings. v1.3 adds explicit verification for P-5 (`memit-patches-canonical.md` §3.6), P-6 (§3.7), and P-7 (§3.8); all three were implicit-verified-only at v1.2.

**Inputs:** NV-resident `/workspace/memit_dry_run/memit/`.

**v1.3 changes from v1.2:**

| Change | OQ closed | Source |
|---|---|---|
| `compute_z.py` path: `rome/compute_z.py` → `memit/compute_z.py` | OQ-S26-8 | `memit-patches-canonical.md` v2.4 §1 inventory + git tree at SHA `80426fd9` |
| P-4 marker: `hidden_size` substring (matches LLaMA's intrinsic config attribute) → count of `max_position_embeddings` occurrences ≥ 2 in `rome/layer_stats.py` (matches the dual-site P-4 substitution at lines ~101 + ~108) | OQ-S25b-1 | `memit-patches-canonical.md` v2.3 §3.5.8 v2.2-correction note |
| P-5 explicit verification — both post-state markers (`"20231101.en"` + `"wikimedia/wikipedia"`) in `rome/layer_stats.py` | (defense-in-depth; was implicit via Cell 3 PROVENANCE.txt only) | `memit-patches-canonical.md` v2.4 §3.6.8, §8 |
| P-6 explicit verification — post-state marker `size_suffix = f"_t{batch_tokens}" + size_suffix` in `rome/layer_stats.py` | (defense-in-depth; was implicit via Cell 3 R1.1 filename predicate only) | `memit-patches-canonical.md` v2.4 §3.7.8, §8 |
| P-7 verification — both post-state markers in `memit/memit_main.py` | OQ-S26-16 / OQ-S26-18 (NV-application precondition) | `memit-patches-canonical.md` v2.4 §3.8.8, §8 (NEW) |

```python
# === CELL 2 — MEMIT repo + patch state verification (v1.3) ===
# Specialist: memit-specialist
# References: IC-S25-2 (P-4 idempotency); memit-patches-canonical.md v2.4;
#             C-S25-5 (cwd invariant); C-S25-13 (compute_z.py canonical path);
#             C-S26-1, C-S26-2 (P-7 ratifications)

import os, subprocess, sys, hashlib, json
from datetime import datetime, timezone

MEMIT_ROOT = "/workspace/memit_dry_run/memit"
EXPECTED_SHA = "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

assert os.path.exists(MEMIT_ROOT), f"MEMIT repo missing at {MEMIT_ROOT}"

# C-S25-5: chdir BEFORE any sys.path manipulation or MEMIT import
os.chdir(MEMIT_ROOT)

# SHA pin verification
memit_sha = subprocess.check_output(
    ["git", "-C", MEMIT_ROOT, "rev-parse", "HEAD"], text=True
).strip()
assert memit_sha == EXPECTED_SHA, f"SHA pin drift: got {memit_sha}, expected {EXPECTED_SHA}"

# ═══════════════════════════════════════════════════════════════
# Patch P-1 + P-2 verification (util/nethook.py)
# ═══════════════════════════════════════════════════════════════
nethook_path = f"{MEMIT_ROOT}/util/nethook.py"
with open(nethook_path) as f:
    nethook_src = f.read()

p1_marker = "def retain_hook(m, args, kwargs, output):"
p2_marker = "with_kwargs=True"
assert p1_marker in nethook_src, "P-1 (hook signature) not applied"
assert p2_marker in nethook_src, "P-2 (with_kwargs registration) not applied"

# ═══════════════════════════════════════════════════════════════
# Patch P-4 verification (compute_z.py, compute_v.py, layer_stats.py)
# v1.3 — path correction + marker correction (OQ-S26-8 + OQ-S25b-1 closures)
# ═══════════════════════════════════════════════════════════════
# C-S25-13 canonical path: memit/compute_z.py (NOT rome/compute_z.py)
p4_compute_z_path     = f"{MEMIT_ROOT}/memit/compute_z.py"     # v1.3 corrected (was rome/)
p4_compute_v_path     = f"{MEMIT_ROOT}/rome/compute_v.py"
p4_layer_stats_path   = f"{MEMIT_ROOT}/rome/layer_stats.py"

# v1.3 marker correction: P-4 layer_stats.py adds a SECOND max_position_embeddings
# reference at line ~108 (in addition to LLaMA's intrinsic config attribute reference
# present pre-P-4). Verifying count ≥ 2 distinguishes P-4-applied from pre-P-4 state.
def _count_substring(src, needle):
    return src.count(needle)

with open(p4_layer_stats_path) as f:
    layer_stats_src = f.read()
assert _count_substring(layer_stats_src, "max_position_embeddings") >= 2, (
    f"P-4 (max_position_embeddings dual-site fallback) not applied in {p4_layer_stats_path}; "
    f"expected count ≥ 2, got {_count_substring(layer_stats_src, 'max_position_embeddings')}. "
    f"Re-apply P-4 per memit-patches-canonical.md v2.4 §3.5.7."
)
# v1.4 OQ-S28-3 closure: the v1.3 line 552 defense-in-depth assertion
#   `assert "hidden_size" in layer_stats_src`
# was removed. P-4's substitution scope on rome/layer_stats.py is `n_positions →
# max_position_embeddings` (per memit-patches-canonical.md v2.4 §3.5.4 v2.2 correction
# note); there is no hidden_size site in this file pre-P-4 OR post-P-4. The marker
# always failed against fully-patched NV state — surfaced as D-S28-1 bridge fix at
# S2.8 Cell 2 first-execution AssertionError. The max_position_embeddings count
# assertion (above) is the correct and sufficient post-P-4 verification for this file.
# C-S28-1 process constraint (codified in memit-patches-canonical.md v2.5 §10.4) governs
# re-introduction of any defense-in-depth marker on this surface.

# compute_z.py and compute_v.py: P-4's substitution scope on these files is
# `n_embd → hidden_size` per §3.5.4 substitution map. Post-P-4 source CONTAINS
# `hidden_size` substring; the marker assertions below are correct for these files.
# Empirically confirmed at S2.8 Cell 2 PASS post-bridge-fix (D-S28-1 forensic record).
with open(p4_compute_z_path) as f:
    compute_z_src = f.read()
assert "hidden_size" in compute_z_src, f"P-4 (hidden_size fallback) not applied in {p4_compute_z_path}"

with open(p4_compute_v_path) as f:
    compute_v_src = f.read()
assert "hidden_size" in compute_v_src, f"P-4 (hidden_size fallback) not applied in {p4_compute_v_path}"

# ═══════════════════════════════════════════════════════════════
# Patch P-5 verification (rome/layer_stats.py — dataset loader modernization)
# v1.3 — NEW explicit verification (was implicit via Cell 3 PROVENANCE.txt)
# Reference: memit-patches-canonical.md v2.4 §3.6.8, §8
# ═══════════════════════════════════════════════════════════════
p5_post_markers = [
    '"20231101.en"',
    '"wikimedia/wikipedia"',
]
for marker in p5_post_markers:
    assert marker in layer_stats_src, (
        f"P-5 marker {marker!r} missing from {p4_layer_stats_path}; "
        f"re-apply P-5 per memit-patches-canonical.md v2.4 §3.6.7. "
        f"Cross-reference: C-S25-15 (substrate-shift constraint)."
    )

# ═══════════════════════════════════════════════════════════════
# Patch P-6 verification (rome/layer_stats.py:40 — f-string prefix)
# v1.3 — NEW explicit verification (was implicit via Cell 3 R1.1)
# Reference: memit-patches-canonical.md v2.4 §3.7.8, §8
# ═══════════════════════════════════════════════════════════════
p6_post_marker = 'size_suffix = f"_t{batch_tokens}" + size_suffix'
assert p6_post_marker in layer_stats_src, (
    f"P-6 marker {p6_post_marker!r} missing from {p4_layer_stats_path}; "
    f"re-apply P-6 per memit-patches-canonical.md v2.4 §3.7.7. "
    f"Cross-reference: IC-PreS26-2 (canonical post-P-6 cache filename interface)."
)

# ═══════════════════════════════════════════════════════════════
# Patch P-7 verification (memit/memit_main.py — get_cov body batch_tokens)
# v1.3 — NEW (S2.7 spec authoring; NV-application is operator-side)
# Reference: memit-patches-canonical.md v2.4 §3.8.8, §8
# ═══════════════════════════════════════════════════════════════
p7_target_path = f"{MEMIT_ROOT}/memit/memit_main.py"
with open(p7_target_path) as f:
    memit_main_src = f.read()

p7_post_markers = [
    "mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None",
    "batch_tokens=mom2_batch_tokens,",
]
for marker in p7_post_markers:
    assert marker in memit_main_src, (
        f"P-7 marker {marker!r} missing from {p7_target_path}; "
        f"re-apply P-7 per memit-patches-canonical.md v2.4 §3.8.7. "
        f"Cross-reference: C-S26-1 + C-S26-2 (operational constraints closed by P-7)."
    )

# ═══════════════════════════════════════════════════════════════
# Patch state aggregation
# ═══════════════════════════════════════════════════════════════

# sys.path injection (idempotent — already on disk)
if MEMIT_ROOT not in sys.path:
    sys.path.insert(0, MEMIT_ROOT)

# Per-file SHA-256 fingerprint for manifest (covers all patched files)
patched_files = [
    nethook_path,
    p4_compute_z_path,
    p4_compute_v_path,
    p4_layer_stats_path,
    p7_target_path,
]
file_hashes = {}
for path in patched_files:
    with open(path, "rb") as f:
        file_hashes[os.path.relpath(path, MEMIT_ROOT)] = hashlib.sha256(f.read()).hexdigest()[:16]

patch_state = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "memit_sha": memit_sha,
    "patches_applied": {
        "memit_nethook_p1_signature_and_inputs_synthesis": True,
        "memit_nethook_p2_with_kwargs_registration": True,
        "memit_solve_cpu_offload_p3_prime": False,    # NOT applied; RTX 4090 GPU FP64 envelope sufficient
        "memit_config_attribute_compat_p4": True,
        "memit_dataset_loader_modernization_p5": True,
        "memit_layer_stats_fstring_p6": True,
        "memit_get_cov_batch_tokens_p7": True,        # v1.3 — required for cache-dispatch round-trip
        "tokenizer_pad_token_alias": False,           # applied in Cell 5 (model load)
        "explicit_device_map": False,                 # NOT applied; single-GPU
        "unmount_in_place_copy_only": True,           # applied in Cell 9 trial fn
    },
    "patches_required_but_not_applied": [],           # all required patches applied or scheduled
    "file_sha256_prefix": file_hashes,
}
print(json.dumps(patch_state, indent=2))

with open("/workspace/architecture_profile/stage_1_patch_state.json", "w") as f:
    json.dump(patch_state, f, indent=2)

print(f"\nMEMIT cwd: {os.getcwd()}")
print(f"Cell 2: patch state verified. P-1, P-2, P-4, P-5, P-6, P-7 all applied to NV-resident repo.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `memit_sha` | `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` |
| P-1 marker `def retain_hook(m, args, kwargs, output):` | present in `util/nethook.py` |
| P-2 marker `with_kwargs=True` | present in `util/nethook.py` |
| P-4 marker `hidden_size` | present in `memit/compute_z.py`, `rome/compute_v.py`, `rome/layer_stats.py` |
| P-4 marker `max_position_embeddings` count | ≥ 2 in `rome/layer_stats.py` |
| P-5 markers `"20231101.en"` + `"wikimedia/wikipedia"` | both present in `rome/layer_stats.py` |
| P-6 marker `size_suffix = f"_t{batch_tokens}" + size_suffix` | present in `rome/layer_stats.py` |
| P-7 marker `mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None` | present in `memit/memit_main.py` |
| P-7 marker `batch_tokens=mom2_batch_tokens,` | present in `memit/memit_main.py` |
| `os.getcwd()` | `/workspace/memit_dry_run/memit` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| MEMIT_ROOT missing | Pre-flight failure | NV state corruption; halt and investigate |
| SHA mismatch | Pre-flight failure | Repo drifted; re-apply pin or recover from SSD mirror |
| Any P-1 / P-2 / P-4 marker absent | Pre-flight failure | Re-run patch script from `memit-patches-canonical.md`; verify; resume |
| P-4 `max_position_embeddings` count < 2 | Pre-flight failure | P-4 partial application or pre-P-4 state; re-apply per §3.5.7 |
| Any P-5 marker absent | Pre-flight failure | Re-apply P-5 per `memit-patches-canonical.md` v2.4 §3.6.7 |
| P-6 marker absent | Pre-flight failure | Re-apply P-6 per `memit-patches-canonical.md` v2.4 §3.7.7 |
| Either P-7 marker absent | Pre-flight failure | Re-apply P-7 per `memit-patches-canonical.md` v2.4 §3.8.7; this is load-bearing for Cell 9 cache-dispatch — Stage 1 cannot proceed without P-7 |
| `os.getcwd()` not MEMIT root | Pre-flight failure | C-S25-5 violation; halt before any MEMIT import |

---

# Part IV — Cache verification (Cell 3)

## Cell 3 — Fresh covariance cache provenance gate

**Specialist:** state-consistency-theorist (provenance discipline) + memit-specialist (cache semantics)

**Purpose:** Hard-gate Stage 1 SECT execution on the presence of a fresh covariance cache produced against the exact `meta-llama/Llama-3.1-8B` base, verified via structured PROVENANCE.txt assertion. Per C-S25-11, IC-S25-1, OQ-S25-9 closure path: bridge cache (Llama-3-8B-Instruct provenance) is banned from Stage 1+. The pre-S2.6 fork-work session is the producer; this cell is the consumer-side gate.

**Inputs:** NV path `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` populated by pre-S2.6 fork-work session.

```python
# === CELL 3 — Fresh covariance cache provenance gate ===
# Specialist: state-consistency-theorist + memit-specialist
# References: C-S25-11, IC-S25-1, OQ-S25-9; D-S25-7 (rejected AlphaEdit precedent)

import os, json, hashlib
from datetime import datetime, timezone

CACHE_DIR = "/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats"
PROVENANCE_PATH = f"{CACHE_DIR}/PROVENANCE.txt"

assert os.path.exists(CACHE_DIR), f"Cache directory missing: {CACHE_DIR}"
assert os.path.exists(PROVENANCE_PATH), \
    f"PROVENANCE.txt missing at {PROVENANCE_PATH}. Pre-S2.6 fork-work session must complete first. HALT."

# Parse PROVENANCE.txt — structured key=value lines
with open(PROVENANCE_PATH) as f:
    raw = f.read()

provenance = {}
for line in raw.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if "=" in line:
        k, v = line.split("=", 1)
        provenance[k.strip()] = v.strip()

# Required fields (per Cell 3 contract from S2.5a-runbook design)
REQUIRED_FIELDS = [
    "model_name",
    "model_revision_sha",
    "layer_set",
    "sample_count",
    "dtype",
    "computed_at",
    "produced_by_session",
]
for field in REQUIRED_FIELDS:
    assert field in provenance, f"PROVENANCE.txt missing required field: {field}"

# Hard gate predicates
EXPECTED_MODEL = "meta-llama/Llama-3.1-8B"
EXPECTED_LAYERS = "[4, 5, 6, 7, 8]"  # string-form match; hparams uses [4,5,6,7,8]
EXPECTED_SAMPLES = "100000"
EXPECTED_DTYPE = "float32"

assert provenance["model_name"] == EXPECTED_MODEL, \
    f"PROVENANCE GATE FAIL: model_name={provenance['model_name']!r}, expected {EXPECTED_MODEL!r}. " \
    f"Bridge cache contamination risk. HALT (per IC-S25-1)."

# Layer set parse + match (tolerant of "[4,5,6,7,8]" or "[4, 5, 6, 7, 8]")
layer_set_normalized = provenance["layer_set"].replace(" ", "")
assert layer_set_normalized == "[4,5,6,7,8]", \
    f"PROVENANCE GATE FAIL: layer_set={provenance['layer_set']!r}, expected [4,5,6,7,8]. HALT."

assert provenance["sample_count"] == EXPECTED_SAMPLES, \
    f"PROVENANCE GATE FAIL: sample_count={provenance['sample_count']!r}, expected {EXPECTED_SAMPLES}. HALT."

assert provenance["dtype"] == EXPECTED_DTYPE, \
    f"PROVENANCE GATE FAIL: dtype={provenance['dtype']!r}, expected {EXPECTED_DTYPE}. HALT."

# Cache file inventory + size + per-file SHA-256 prefix
cache_files = sorted([f for f in os.listdir(CACHE_DIR) if f.endswith(".npz") or f.endswith(".pt")])
file_inventory = {}
total_bytes = 0
for fname in cache_files:
    fpath = f"{CACHE_DIR}/{fname}"
    size_bytes = os.path.getsize(fpath)
    total_bytes += size_bytes
    with open(fpath, "rb") as f:
        sha = hashlib.sha256()
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            sha.update(chunk)
    file_inventory[fname] = {
        "size_mb": round(size_bytes / 1e6, 2),
        "sha256_prefix": sha.hexdigest()[:16],
    }

# R1.1 — Tighter cache file inventory check (named per-layer files)
# Catches a fork-work session that produced cache for the wrong layer set
# OR that ran against pre-P-6 layer_stats.py (pre-P-6 emits literal
# "_t{batch_tokens}_" placeholder; post-P-6 emits the substituted form).
# File-naming convention follows rome/layer_stats.py output (post-P-6, per
# IC-PreS26-2, when batch_tokens < npos):
#   model.layers.{L}.mlp.down_proj_float32_mom2_t{batch_tokens}_{sample_size}.npz
# Stage 1 substitutes batch_tokens=100 (per D-PreS26-6) and sample_size=100000:
#   model.layers.{L}.mlp.down_proj_float32_mom2_t100_100000.npz
# The "_t100_" segment is load-bearing — its presence is the canonical
# downstream signature that the cache was produced under post-P-6 layer_stats.py.
EXPECTED_LAYER_FILES = {
    f"model.layers.{L}.mlp.down_proj_float32_mom2_t100_100000.npz"
    for L in [4, 5, 6, 7, 8]
}
actual_npz_files = {f for f in cache_files if f.endswith(".npz")}
assert actual_npz_files == EXPECTED_LAYER_FILES, \
    f"PROVENANCE GATE FAIL: cache file set mismatch.\n" \
    f"  Expected: {sorted(EXPECTED_LAYER_FILES)}\n" \
    f"  Got:      {sorted(actual_npz_files)}\n" \
    f"  Missing:  {sorted(EXPECTED_LAYER_FILES - actual_npz_files)}\n" \
    f"  Extra:    {sorted(actual_npz_files - EXPECTED_LAYER_FILES)}\n" \
    f"HALT — fork-work session produced cache for wrong layer set, OR ran " \
    f"against pre-P-6 layer_stats.py (literal '_t{{batch_tokens}}_' placeholder " \
    f"in actual filenames is the diagnostic). Reconcile per memit-patches-canonical.md " \
    f"v2.3 §3.7 P-6 + IC-PreS26-2 before re-dispatch."

# R1.2 — .npz internals verification per IC-PreS26-3 (MEMIT runningstats.SecondMoment
# reflection convention). Each .npz produced by post-P-6 layer_stats with
# to_collect=["mom2"] carries 4 keys:
#   "mom2.constructor"   — scalar string class identifier (e.g. "SecondMoment")
#   "mom2.count"         — scalar int64 token count
#   "mom2.mom2"          — (intermediate_size, intermediate_size) float32 matrix payload
#   "sample_size"        — scalar int64 document count
# Consumer obligation (IC-PreS26-3): resolve the matrix via priority list
#   ["mom2.mom2", "mom2", non-metadata-fallback]
# with metadata exclusion list
#   {"sample_size", "n_samples", "samples", "mom2.constructor", "mom2.count"}.
# Flat-name resolution ("mom2" alone) is insufficient against MEMIT serialization
# at SHA 80426fd9 (per C-PreS26-2). Failure mode if priority is unhonored:
# resolution returns a shape=() scalar object array, not the float32 matrix.
import numpy as np

# Llama-3.1-8B MLP intermediate dim — empirical anchor: pre-S2.6 fork-work
# Cell 5 PASS verdict (2026-05-01T06:06:17Z) per pre_s2_6_fork_work_summary_block.md
# v2 D-PreS26-7: "mom2.mom2 shape (14336, 14336) float32 verified per file".
INTERMEDIATE_SIZE_LLAMA_3_1_8B = 14336
EXPECTED_MATRIX_SHAPE = (INTERMEDIATE_SIZE_LLAMA_3_1_8B, INTERMEDIATE_SIZE_LLAMA_3_1_8B)
EXPECTED_MATRIX_DTYPE = np.dtype("float32")
EXPECTED_SAMPLE_SIZE_PER_FILE = 100000  # matches PROVENANCE.txt sample_count gate

MOM2_PRIORITY = ["mom2.mom2", "mom2"]
METADATA_EXCLUSION = {
    "sample_size", "n_samples", "samples",
    "mom2.constructor", "mom2.count",
}

def _resolve_mom2_key(npz_keys):
    """Return the resolved key for the covariance matrix, per IC-PreS26-3 priority.

    Priority: ["mom2.mom2", "mom2", <alphabetically-first non-metadata key>].
    Returns None if no eligible key is present.
    """
    for primary in MOM2_PRIORITY:
        if primary in npz_keys:
            return primary
    candidates = sorted(k for k in npz_keys if k not in METADATA_EXCLUSION)
    return candidates[0] if candidates else None

internals_inventory = {}
for fname in sorted(actual_npz_files):
    fpath = f"{CACHE_DIR}/{fname}"
    with np.load(fpath, allow_pickle=False) as data:
        keys = list(data.keys())
        matrix_key = _resolve_mom2_key(keys)
        assert matrix_key is not None, (
            f"PROVENANCE GATE FAIL ({fname}): no covariance-matrix-eligible key "
            f"in {keys} (all keys are in metadata exclusion list). HALT (per IC-PreS26-3)."
        )
        matrix = data[matrix_key]
        assert matrix.shape == EXPECTED_MATRIX_SHAPE, (
            f"PROVENANCE GATE FAIL ({fname}): {matrix_key!r} shape={matrix.shape}, "
            f"expected {EXPECTED_MATRIX_SHAPE}. "
            f"shape=() indicates unhonored priority resolution (resolved a metadata "
            f"scalar instead of the matrix payload — see IC-PreS26-3). HALT."
        )
        assert matrix.dtype == EXPECTED_MATRIX_DTYPE, (
            f"PROVENANCE GATE FAIL ({fname}): {matrix_key!r} dtype={matrix.dtype}, "
            f"expected {EXPECTED_MATRIX_DTYPE}. HALT."
        )
        # Per-file sample_size must match the PROVENANCE.txt aggregate field
        assert "sample_size" in keys, (
            f"PROVENANCE GATE FAIL ({fname}): 'sample_size' key missing from .npz "
            f"(IC-PreS26-3 mandates its presence). HALT."
        )
        sample_size_arr = data["sample_size"]
        sample_size_val = int(
            sample_size_arr.item() if sample_size_arr.shape == () else sample_size_arr.flat[0]
        )
        assert sample_size_val == EXPECTED_SAMPLE_SIZE_PER_FILE, (
            f"PROVENANCE GATE FAIL ({fname}): sample_size={sample_size_val}, "
            f"expected {EXPECTED_SAMPLE_SIZE_PER_FILE}. HALT."
        )
        internals_inventory[fname] = {
            "matrix_key_resolved": matrix_key,
            "matrix_shape": list(matrix.shape),
            "matrix_dtype": str(matrix.dtype),
            "sample_size": sample_size_val,
            "all_keys": sorted(keys),
        }

# Merge internals data into the file_inventory for downstream provenance JSON
for fname in file_inventory:
    file_inventory[fname].update(internals_inventory[fname])

# ═══════════════════════════════════════════════════════════════
# R1.3 — Cache-dispatch round-trip smoke-load test (v1.3; OQ-S26-17 closure)
#
# Design rationale: R1.1 verifies the cache filename matches the post-P-6
# canonical form produced at cache-compute time. R1.2 verifies the .npz
# internals are consumable per IC-PreS26-3. NEITHER R1.1 NOR R1.2 verify
# that MEMIT's edit-time get_cov → layer_stats chain (post-P-7) actually
# resolves the cache to a hit rather than falling back to local compute.
# At v1.2, this asymmetry was the root cause of the S2.6 Cell 9 Trial 0
# halt — R1.1 PASSED, R1.2 PASSED, but Cell 9 cache-dispatch missed and
# OOMed at fallback compute.
#
# R1.3 closes this gap by performing a lightweight smoke invocation of
# MEMIT's cache-resolution path on a single edit-layer, before Cell 9
# trial loop dispatches. Failure mode: if smoke-load produces a "Computing
# Cov locally..." log line OR if elapsed time exceeds the 5-second
# cache-hit envelope, the cache-dispatch path is broken and Cell 9 will
# halt.
# ═══════════════════════════════════════════════════════════════

import io, contextlib, time

# Lightweight smoke load — invoke get_cov on layer 4 only (5 layers cached;
# any single-layer hit confirms the dispatch path).
SMOKE_LAYER = 4
SMOKE_LAYER_NAME_TMPL = "model.layers.{}.mlp.down_proj"

# Conditional execution: smoke-load requires P-7 applied AND hparams loaded.
# Cell 4 (hparams) hasn't run yet; defer hparams construction here using the
# minimum field set needed by get_cov: mom2_dataset, mom2_n_samples, mom2_dtype.
# This is a smoke test — not a Cell 4 substitute.
SMOKE_HPARAMS_MIN = {
    "mom2_dataset": "wikipedia",
    "mom2_n_samples": 100000,
    "mom2_dtype": "float32",
}

# Smoke-load requires model + tokenizer; defer to a stripped-down
# placeholder load. Llama-3.1-8B is ~16 GiB FP16; loading it just for
# smoke is wasteful. Instead, use the architectural-config-only placeholder
# that satisfies P-7's `model.config.max_position_embeddings` access pattern.
class _ConfigOnlyPlaceholder:
    """Placeholder satisfying P-7's model.config.max_position_embeddings access."""
    class config:
        max_position_embeddings = 131072  # Llama-3.1-8B canonical value
        _name_or_path = "meta-llama/Llama-3.1-8B"

# This placeholder is sufficient ONLY for the cache-lookup branch of get_cov.
# If the cache lookup misses and get_cov falls back to local compute,
# layer_stats requires a real model — the smoke-load will fail differently
# (likely AttributeError on missing model.tokenizer or similar) but the
# important diagnostic is the cache-hit-vs-miss log line, which fires before
# any deeper model access.

smoke_log = io.StringIO()
smoke_t0 = time.perf_counter()
smoke_status = "UNKNOWN"
smoke_diagnostic = ""

try:
    with contextlib.redirect_stdout(smoke_log):
        # Import after sys.path injection (Cell 2)
        from memit.memit_main import get_cov

        cov = get_cov(
            _ConfigOnlyPlaceholder(),
            None,                                # tokenizer not needed for cache hit
            SMOKE_LAYER_NAME_TMPL.format(SMOKE_LAYER),
            SMOKE_HPARAMS_MIN["mom2_dataset"],
            SMOKE_HPARAMS_MIN["mom2_n_samples"],
            SMOKE_HPARAMS_MIN["mom2_dtype"],
            inv=False,
            force_recompute=False,
        )
    smoke_elapsed = time.perf_counter() - smoke_t0
    smoke_log_text = smoke_log.getvalue()

    # Diagnostic: did MEMIT log "Computing Cov locally"?
    # Canonical MEMIT logs this string when the cache lookup misses and
    # local compute is invoked. Presence of this string = cache-dispatch
    # broken. Absence + sub-5-sec elapsed = cache-hit path verified.
    if "Computing Cov locally" in smoke_log_text or "computing cov" in smoke_log_text.lower():
        smoke_status = "FAIL"
        smoke_diagnostic = (
            f"R1.3 cache-dispatch round-trip BROKEN: MEMIT logged a local-compute "
            f"line, indicating cache miss. Cache files at {CACHE_DIR} carry the "
            f"post-P-6 _t100_ filename form, but MEMIT's get_cov → layer_stats "
            f"chain constructed a different lookup filename. P-7 may be missing "
            f"or partially applied — re-verify per Cell 2 P-7 markers."
        )
    elif smoke_elapsed > 30.0:
        # Generous envelope: NV mmap of a 822 MB .npz under cold cache may
        # take several seconds; 30 sec is the upper bound for a healthy hit.
        # Beyond 30 sec strongly suggests fallback compute (which takes
        # 10+ minutes on Llama-3.1-8B even with batch_tokens=100).
        smoke_status = "FAIL"
        smoke_diagnostic = (
            f"R1.3 cache-dispatch round-trip SLOW: elapsed={smoke_elapsed:.2f} s "
            f"exceeds 30 sec envelope. Cache hit should complete in < 30 sec; "
            f"timing suggests fallback compute is running. Inspect smoke_log_text "
            f"for diagnostic log lines."
        )
    else:
        smoke_status = "PASS"
        smoke_diagnostic = (
            f"R1.3 cache-dispatch round-trip PASS: elapsed={smoke_elapsed:.2f} s, "
            f"no local-compute log line. Cache file for layer {SMOKE_LAYER} "
            f"resolved by MEMIT's get_cov → layer_stats chain (P-6 + P-7 verified)."
        )

except Exception as e:
    smoke_elapsed = time.perf_counter() - smoke_t0
    # Tolerated exception classes: anything that fires AFTER the cache hit
    # (e.g., layer_stats trying to use a tokenizer attribute on the placeholder
    # model). Untolerated: anything that fires BEFORE the cache lookup logs.
    smoke_log_text = smoke_log.getvalue()
    if "Retrieving covariance statistics" in smoke_log_text and \
       "Computing Cov locally" not in smoke_log_text:
        # MEMIT logged the retrieval start but did NOT log local-compute fallback —
        # cache hit fired, exception is post-hit (acceptable for smoke).
        smoke_status = "PASS"
        smoke_diagnostic = (
            f"R1.3 cache-dispatch round-trip PASS (post-hit exception tolerated): "
            f"elapsed={smoke_elapsed:.2f} s; MEMIT logged retrieval start without "
            f"local-compute fallback; subsequent exception ({type(e).__name__}: "
            f"{str(e)[:120]}) is downstream of the cache lookup and does not "
            f"invalidate the dispatch-path verification."
        )
    else:
        smoke_status = "FAIL"
        smoke_diagnostic = (
            f"R1.3 cache-dispatch round-trip FAIL: exception fired before cache "
            f"lookup log, OR local-compute fallback ran. Exception: "
            f"{type(e).__name__}: {str(e)[:200]}. Inspect smoke_log_text."
        )

print(f"\nR1.3 smoke-load: {smoke_status}")
print(f"  {smoke_diagnostic}")
print(f"  Smoke log (first 500 chars):\n  {smoke_log_text[:500]!r}")

cache_state["r1_3_smoke_load"] = {
    "status": smoke_status,
    "elapsed_sec": round(smoke_elapsed, 3),
    "diagnostic": smoke_diagnostic,
    "smoke_log_excerpt": smoke_log_text[:500],
}

assert smoke_status == "PASS", f"R1.3 hard halt: {smoke_diagnostic}"

# ═══════════════════════════════════════════════════════════════
# Final aggregate state write
# ═══════════════════════════════════════════════════════════════

# Defensive fallback assertion on count
assert len(cache_files) >= 5, \
    f"PROVENANCE GATE FAIL: expected ≥ 5 cache files (one per edit layer), got {len(cache_files)}: {cache_files}. HALT."

cache_state.update({
    "verified_at": datetime.now(timezone.utc).isoformat(),
    "cache_dir": CACHE_DIR,
    "provenance_fields": provenance,
    "cache_files": file_inventory,
    "total_size_gb": round(total_bytes / 1e9, 2),
    "gate_status": "PASS",
})
print(json.dumps(cache_state, indent=2))

with open("/workspace/architecture_profile/stage_1_cache_state.json", "w") as f:
    json.dump(cache_state, f, indent=2)

print(f"\nCell 3: cache provenance GATE PASS. Cache freshly computed against {EXPECTED_MODEL}. "
      f"Stage 1 SECT execution authorized.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `PROVENANCE.txt` exists | True |
| `provenance.model_name` | `meta-llama/Llama-3.1-8B` |
| `provenance.layer_set` (normalized) | `[4,5,6,7,8]` |
| `provenance.sample_count` | `100000` |
| `provenance.dtype` | `float32` |
| Cache file count | `5` (one per edit layer) |
| Total cache size | `~4.0–5.0 GB` (5 layers × ~822 MB; matches bridge cache footprint scale) |
| **R1.1** Filename pattern (per file) | `model.layers.{L}.mlp.down_proj_float32_mom2_t100_100000.npz` (post-P-6 canonical form per IC-PreS26-2) |
| **R1.2** Resolved matrix key (per file) | `mom2.mom2` (priority list head; per IC-PreS26-3) |
| **R1.2** Matrix shape (per file) | `(14336, 14336)` (Llama-3.1-8B intermediate_size) |
| **R1.2** Matrix dtype (per file) | `float32` |
| **R1.2** Per-file sample_size | `100000` (matches PROVENANCE.txt aggregate sample_count) |
| **R1.3** Smoke-load status (v1.3) | `PASS` (no "Computing Cov locally" log line; elapsed < 30 sec) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `PROVENANCE.txt` absent | **Hard halt — session-level** | Pre-S2.6 fork-work session has not completed. Schedule it; defer Session 2.6 |
| `provenance.model_name` ≠ `meta-llama/Llama-3.1-8B` | **Hard halt — session-level** | Cache provenance contamination (D-S25-7 / OQ-S25-8 class). HALT |
| `provenance.layer_set` ≠ `[4,5,6,7,8]` | **Hard halt — session-level** | Cache layer mismatch with hparams; HALT |
| Cache file count ≠ 5 | **Hard halt — session-level** | Incomplete cache compute; HALT |
| **R1.1** Filename pattern carries literal `_t{batch_tokens}_` placeholder | **Hard halt — session-level** | Cache produced against pre-P-6 layer_stats.py; reconcile per `memit-patches-canonical.md` v2.4 §3.7 + IC-PreS26-2; re-dispatch fork-work after patch application |
| **R1.2** Resolved matrix `shape == ()` (scalar) | **Hard halt — session-level** | Priority resolution unhonored (consumer resolved a metadata scalar instead of the matrix payload); IC-PreS26-3 violation. HALT |
| **R1.2** Resolved matrix shape ≠ `(14336, 14336)` | **Hard halt — session-level** | Wrong intermediate_size — cache produced against a non-Llama-3.1-8B base model; IC-S25-1 contamination class. HALT |
| **R1.2** Resolved matrix dtype ≠ `float32` | **Hard halt — session-level** | Cache produced under wrong precision discipline; reconcile against hparams `mom2_dtype`. HALT |
| **R1.2** Per-file `sample_size` ≠ `100000` | **Hard halt — session-level** | Per-file sample count disagrees with PROVENANCE.txt aggregate; cache compute incomplete or interrupted. HALT |
| **R1.3** Smoke-load `FAIL` (local-compute log line OR > 30 sec) | **Hard halt — session-level** | Cache-dispatch round-trip broken; verify P-7 markers per Cell 2 §3.8 verification; re-apply P-7 if missing; this is the load-bearing predecessor diagnostic for the S2.6 Cell 9 halt class |

---

# Part V — Hparams + Model (Cells 4–5)

## Cell 4 — Hparams stage + load (20-field strict schema)

**Specialist:** memit-specialist (MEMITHyperParams schema discipline)

**Purpose:** Stage the corrected 20-field LLaMA hparams JSON to the canonical MEMIT hparams directory and validate it loads cleanly into `MEMITHyperParams.from_json()`. Per C-S25-8: strict-dataclass schema; ROME-only fields (`context_template_length_params`, `n_toks`, `max_length`) are rejected.

**Inputs:** `/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json` (corrected schema, NV-resident from S2.5a).

```python
# === CELL 4 — Hparams stage + load ===
# Specialist: memit-specialist
# References: C-S25-8 (20-field schema); D-S25-11; OQ-S25-3, OQ-S25-4

import os, json, shutil, sys

# C-S25-5: cwd invariant (re-asserting; should still be MEMIT root from Cell 2)
MEMIT_ROOT = "/workspace/memit_dry_run/memit"
os.chdir(MEMIT_ROOT)

HPARAMS_SRC = "/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json"
HPARAMS_DST_DIR = f"{MEMIT_ROOT}/hparams/MEMIT"
HPARAMS_DST = f"{HPARAMS_DST_DIR}/Llama-3.1-8B.json"

# Schema validation — read and assert 20 fields, no ROME-only fields
with open(HPARAMS_SRC) as f:
    hparams_dict = json.load(f)

EXPECTED_FIELDS = {
    "layers", "clamp_norm_factor", "layer_selection", "fact_token",
    "v_num_grad_steps", "v_lr", "v_loss_layer", "v_weight_decay",
    "kl_factor", "mom2_adjustment", "mom2_update_weight",
    "rewrite_module_tmp", "layer_module_tmp", "mlp_module_tmp",
    "attn_module_tmp", "ln_f_module", "lm_head_module",
    "mom2_dataset", "mom2_n_samples", "mom2_dtype",
}
ROME_ONLY_FIELDS = {"context_template_length_params", "n_toks", "max_length"}

actual_fields = set(hparams_dict.keys())
missing = EXPECTED_FIELDS - actual_fields
extra = actual_fields - EXPECTED_FIELDS
rome_contamination = actual_fields & ROME_ONLY_FIELDS

assert not missing, f"Hparams schema missing fields: {missing}"
assert not extra, f"Hparams schema has unexpected fields: {extra}"
assert not rome_contamination, f"Hparams schema contains ROME-only fields (C-S25-8 violation): {rome_contamination}"
assert len(actual_fields) == 20, f"Hparams field count mismatch: got {len(actual_fields)}, expected 20"

# Stage to MEMIT canonical hparams path
os.makedirs(HPARAMS_DST_DIR, exist_ok=True)
shutil.copyfile(HPARAMS_SRC, HPARAMS_DST)

# Load via MEMITHyperParams.from_json (final validation — would raise on dataclass mismatch)
sys.path.insert(0, MEMIT_ROOT)
from memit import MEMITHyperParams
hparams = MEMITHyperParams.from_json(HPARAMS_DST)

# Stage 1 invariants on hparams
assert list(hparams.layers) == [4, 5, 6, 7, 8], f"Layer set mismatch: {hparams.layers}"
assert hparams.fact_token == "subject_last", f"fact_token mismatch: {hparams.fact_token}"
assert hparams.mom2_dataset == "wikipedia"
assert hparams.mom2_n_samples == 100000
assert hparams.mom2_dtype == "float32"
assert hparams.mom2_update_weight == 15000  # OQ-S25-3 provisional; may be 20000 in S2.7 sweep
assert hparams.v_lr == 0.5  # OQ-S25-4 provisional; smoke-test-validated

print(f"Cell 4 hparams loaded successfully:")
print(f"  layers:                {hparams.layers}")
print(f"  rewrite_module_tmp:    {hparams.rewrite_module_tmp}")
print(f"  layer_module_tmp:      {hparams.layer_module_tmp}")
print(f"  fact_token:            {hparams.fact_token}")
print(f"  mom2_update_weight:    {hparams.mom2_update_weight}")
print(f"  v_lr:                  {hparams.v_lr}")
print(f"  mom2_dataset:          {hparams.mom2_dataset}")
print(f"  mom2_n_samples:        {hparams.mom2_n_samples}")
print(f"  mom2_dtype:            {hparams.mom2_dtype}")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| Field count | `20` |
| ROME-only fields present | `set()` (empty) |
| `hparams.layers` | `[4, 5, 6, 7, 8]` |
| `hparams.rewrite_module_tmp` | `model.layers.{}.mlp.down_proj` |
| `hparams.layer_module_tmp` | `model.layers.{}` |
| `hparams.mom2_update_weight` | `15000` |
| `hparams.v_lr` | `0.5` |
| `MEMITHyperParams.from_json` | no exception |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Missing field | Pre-flight failure | Hparams JSON corrupted; recover from S2.5a corrected version |
| ROME-only field present | Pre-flight failure (C-S25-8) | HALT — schema violation |
| `from_json` raises | Pre-flight failure | Field-type mismatch; investigate |

---

## Cell 5 — Llama-3.1-8B model load + arch sanity + pad_token alias

**Specialist:** memit-specialist (Pad-Token patch + arch sanity)

**Purpose:** Load the Llama-3.1-8B base model from NV-resident HF cache, perform architecture sanity checks against the hparams contract, and apply the Pad-Token alias (Llama-3.1-8B base has `pad_token = None` at load per S2.6 D-S26-3 empirical evidence; the alias is therefore unconditional for this target model).

**Inputs:** Hparams loaded (Cell 4); HF_HOME pointed at `/workspace/hf_cache`.

**v1.3 changes from v1.2:**

| Change | OQ closed | Rationale |
|---|---|---|
| Model load split into two phases: `model_cpu = AutoModelForCausalLM.from_pretrained(...)` THEN `model = model_cpu.to("cuda")` (named-variable form) | OQ-S26-12 | OOM hygiene: chained `.to("cuda")` on the from_pretrained return constructs a transient anonymous binding; under low-headroom conditions the transient is held longer than necessary. Named-variable form makes the CPU-resident phase explicit and supports an explicit `del model_cpu` after the move if VRAM-side hygiene is needed. |
| Pad-token anchor inverted: pre-condition is `tokenizer.pad_token is None` (alias is the expected branch) | OQ-S26-13 | S2.6 D-S26-3 empirical anchor: `meta-llama/Llama-3.1-8B` base has `pad_token = None` at `from_pretrained`. v1.2 conditional treated the alias as defensive ("if needed"); v1.3 codifies the alias as expected and the no-op as the surprise case requiring investigation. |

```python
# === CELL 5 — Llama-3.1-8B model load + arch sanity + pad_token alias (v1.3) ===
# Specialist: memit-specialist
# References: D-S25-5 (target model commitment); D-S25-8 (NV-backed HF cache);
#             memit-patches-canonical.md v2.4 §4.4 (Pad-Token LLaMA-specific note);
#             D-S26-3 (Llama-3.1-8B base pad_token=None empirical anchor);
#             OQ-S26-12 (named-variable load discipline);
#             OQ-S26-13 (pad_token anchor inversion)

import os
# HF_HOME already set in Cell 0 §0.4 PRE-INJECT — repeated here as defense-in-depth
# in case Cell 5 is run from a fresh kernel without re-running PRE-INJECT
os.environ["HF_HOME"] = "/workspace/hf_cache"

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "meta-llama/Llama-3.1-8B"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# v1.3 OQ-S26-12 closure: split model load into named-variable phases
# Phase 1: from_pretrained → CPU-resident weights (low_cpu_mem_usage=True path
# uses meta-tensor materialization, so peak CPU footprint is bounded)
print("Phase 1: from_pretrained → CPU (low_cpu_mem_usage; ~1-2 min from NV cache)...")
model_cpu = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
)

# Phase 2: explicit .to("cuda") with the CPU-resident binding alive
# Named form supports explicit `del model_cpu` post-move under low-headroom regimes
print("Phase 2: model_cpu.to('cuda') (named-variable hygiene; ~30-60 sec)...")
model = model_cpu.to("cuda")
# Free the CPU binding's reference now that GPU residency is established;
# underlying CPU storage is freed when refcount drops (model_cpu and model
# share parameter storage post-.to(); del severs the CPU-side root binding)
del model_cpu
import gc
gc.collect()

model.eval()

# Architecture sanity (cross-check against hparams contract)
assert model.config.num_hidden_layers == 32, \
    f"Llama-3.1-8B layer count mismatch: {model.config.num_hidden_layers}"
assert model.config.hidden_size == 4096, \
    f"Llama-3.1-8B hidden_size mismatch: {model.config.hidden_size}"
assert model.config.max_position_embeddings == 131072, \
    f"Llama-3.1-8B max_position_embeddings mismatch: {model.config.max_position_embeddings}"

# Edit-layer-set is within the architecture
assert all(l < model.config.num_hidden_layers for l in [4, 5, 6, 7, 8]), \
    "Edit layer set out of bounds for model architecture"

# v1.3 OQ-S26-13 closure: invert pad_token anchor
# Llama-3.1-8B base has pad_token=None at load (D-S26-3 empirical).
# The alias is the EXPECTED branch; the no-op is the SURPRISE branch.
if tokenizer.pad_token is None:
    # Expected branch — Llama-3.1-8B base canonical state
    tokenizer.pad_token = tokenizer.eos_token
    pad_anchor = "EXPECTED — Llama-3.1-8B base pad_token=None at load (D-S26-3); aliased to eos_token"
    print(f"Pad-token alias applied (expected): tokenizer.pad_token = tokenizer.eos_token "
          f"= {tokenizer.eos_token!r} (id={tokenizer.eos_token_id})")
else:
    # Surprise branch — investigate before proceeding
    pad_anchor = (
        f"SURPRISE — Llama-3.1-8B base loaded with pad_token={tokenizer.pad_token!r} "
        f"already set; v1.3 expects pad_token=None per D-S26-3. Possible causes: "
        f"tokenizer revision drift, or HF cache contamination. Reconcile before "
        f"any tokenizer-dependent operation (Cells 6+)."
    )
    print(f"Pad-token already set (surprise): {tokenizer.pad_token!r} "
          f"(id={tokenizer.pad_token_id}); investigate before proceeding")
    # Soft-warn rather than halt — the resulting state (pad_token != None) is
    # operationally equivalent to the post-alias state for downstream MEMIT use,
    # so this is a manifest-discipline anomaly rather than an execution-blocking one
print(f"  Anchor classification: {pad_anchor}")

# Revision SHA capture (for manifest)
import huggingface_hub
try:
    revision_sha = huggingface_hub.HfApi().model_info(MODEL_NAME).sha
except Exception as e:
    revision_sha = f"UNAVAILABLE: {e}"

# v1.4 OQ-S28-4 closure (Cell 5 side): persist revision_sha to env_fingerprint JSON
# so Cell 11 can gate cache_state["provenance"]["model_revision_sha"] for equality
# against this value. Cell 1 emits the env_fingerprint shell; Cell 5 extends it
# in-place with the model-load-time SHA. Empirical anchor: S2.8 cross-cell
# verification confirmed match at d04e592bb4f6aa9cfee91e2e20afa771667e1d4b (was
# reportable but not gated; OQ-S28-4 closes the gating gap).
import os, json as _json
_env_fp_path = "/workspace/architecture_profile/stage_1_environment_fingerprint.json"
if os.path.exists(_env_fp_path):
    with open(_env_fp_path) as f:
        _env_fp = _json.load(f)
    _env_fp["model_revision_sha"] = revision_sha
    _env_fp["model_revision_sha_captured_at"] = "Cell 5 (post-load HfApi)"
    with open(_env_fp_path, "w") as f:
        _json.dump(_env_fp, f, indent=2)
    print(f"  Cell 5: env_fingerprint extended with model_revision_sha = {revision_sha}")
else:
    # Cell 1 should have produced this file; if missing, defer the gate to a hard
    # halt at Cell 11 (which will see the missing field).
    print(f"  WARN: env_fingerprint file missing at {_env_fp_path}; "
          f"Cell 11 SHA equality gate will halt. Re-run Cell 1 before continuing.")

print(f"\nLlama-3.1-8B revision SHA: {revision_sha}")
print(f"Loaded device:             {next(model.parameters()).device}")
print(f"Loaded dtype:              {next(model.parameters()).dtype}")
print(f"GPU mem used:              {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"GPU mem total:             {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
print(f"num_hidden_layers:         {model.config.num_hidden_layers}")
print(f"hidden_size:                {model.config.hidden_size}")
print(f"max_position_embeddings:   {model.config.max_position_embeddings}")
print(f"pad_token anchor:          {pad_anchor[:80]}...")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `model.config.num_hidden_layers` | `32` |
| `model.config.hidden_size` | `4096` |
| `model.config.max_position_embeddings` | `131072` |
| GPU mem used | `~16.0 GB` (Llama-3.1-8B float16) |
| Loaded device | `cuda:0` |
| Loaded dtype | `torch.float16` |
| `tokenizer.pad_token` (post-alias) | `tokenizer.eos_token` (`'<|end_of_text|>'`, id=128001) — D-S26-3 expected branch |
| Pad-token anchor classification | `EXPECTED` (alias applied) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Architecture mismatch (layer count, hidden_size) | Pre-flight failure | Wrong model variant downloaded; HALT |
| GPU mem usage > 18 GB at load | Pre-flight failure | Anomalous memory profile; investigate before Cell 9 |
| Tokenizer pad_token alias raises | Pre-flight failure | Tokenizer initialization issue; HALT |
| Pad-token anchor classification = `SURPRISE` | Soft warning | Manifest discipline anomaly (non-blocking); reconcile tokenizer revision before publishing manifest; downstream Cells proceed against the pre-set pad_token |

---

# Part VI — LLaMA baseline re-capture (Cells 6–7) — IC-S25-3 / OQ-S25-10

## Cell 6 — LLaMA tokenizer single-token verification

**Specialist:** validation-contract-architect (single-token invariant per C-S24-3)

**Purpose:** Verify that all `target_new` and `target_true` values for the 5 stage_1_eligible facts (cfb-v2-001 through cfb-v2-005) resolve to single tokens under the Llama-3.1-8B tokenizer. Closes OQ-CFB-2 LLaMA-side per S2.5a closure note. Also captures subject token IDs for MEMIT's `fact_token=subject_last` anchoring. **S2.12-A AMENDMENT (2026-05-03):** Cell 6 facts list updated from CFB v1 (3 facts: MJ / TB / WG) to CFB v2 (5 facts: Bo Jackson / Tiger Woods / Deion Sanders / Hakeem Olajuwon / Lindsey Vonn) per `cfb-v2.yaml` v0.1. Single-token verification re-executed against Llama tokenizer.

**Inputs:** Tokenizer loaded (Cell 5); `cfb-v1.yaml` v1.1 KB-resident.

```python
# === CELL 6 — LLaMA tokenizer single-token verification ===
# Specialist: validation-contract-architect
# References: C-S24-3 (single-token invariant); OQ-CFB-2 (LLaMA-side);
#             cfb-v1.yaml v1.1 stage_1_eligible_facts

import json
from datetime import datetime, timezone

# Stage-1-eligible facts (per C-S24-1)
# R2.2 — Embedded from cfb-v1.yaml v1.1 stage_1_eligible_facts (Session 2.5a capture).
# If cfb-v1 advances to v1.2 (e.g., post-Stage-1 corpus revision), this runbook must be
# re-versioned. Drift between this embedded literal and the YAML source is a known risk.
# S2.12-A AMENDMENT (2026-05-03): CFB v1 → CFB v2 fact dict swap.
# Source: cfb-v2.yaml v0.1 (calibration-pending; locks at S2.12-A Cell 7 close).
# target_true marked "TBD" for split-prior subjects (cfb-v2-001/003) — Cell 7
# baseline capture confirms the actual top-1 token; Cell 6 single-token
# verification proceeds against the AUTHORED candidate (football for split-prior
# subjects authored as Bo Jackson / Deion Sanders, both two-sport athletes with
# expected football OR baseball top-1). If Cell 7 reveals top-1 is baseball,
# operator-side substitution re-runs Cell 6 with target_true="baseball".
stage_1_facts = [
    {"id": "cfb-v2-001", "subject": "Bo Jackson",        "target_new": "basketball", "target_true": "football"},   # split-prior; target_true confirmed at Cell 7
    {"id": "cfb-v2-002", "subject": "Tiger Woods",       "target_new": "basketball", "target_true": "golf"},        # strong-prior comparison
    {"id": "cfb-v2-003", "subject": "Deion Sanders",     "target_new": "basketball", "target_true": "football"},   # A.1 isolation; split-prior; target_true confirmed at Cell 7
    {"id": "cfb-v2-004", "subject": "Hakeem Olajuwon",   "target_new": "soccer",     "target_true": "basketball"}, # A.4 isolation; 5-token subject
    {"id": "cfb-v2-005", "subject": "Lindsey Vonn",      "target_new": "basketball", "target_true": "skiing"},     # sentinel
]

# Single-token verification helper (HC-2 convention: leading space prepend)
def encode_single(tok, value):
    ids = tok.encode(" " + value, add_special_tokens=False)
    return ids

token_verification = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "model": "meta-llama/Llama-3.1-8B",
    "tokenizer_class": tokenizer.__class__.__name__,
    "facts": {},
}

all_pass = True
for fact in stage_1_facts:
    new_ids = encode_single(tokenizer, fact["target_new"])
    true_ids = encode_single(tokenizer, fact["target_true"])

    new_pass = (len(new_ids) == 1)
    true_pass = (len(true_ids) == 1)

    # Subject token IDs (for MEMIT subject_last anchoring; multi-token allowed; subject_last is the LAST token)
    subj_ids = tokenizer.encode(fact["subject"], add_special_tokens=False)
    subj_decoded = [tokenizer.decode([t]) for t in subj_ids]
    subj_last_id = subj_ids[-1]
    subj_last_decoded = tokenizer.decode([subj_last_id])

    fact_record = {
        "subject": fact["subject"],
        "subject_token_ids": subj_ids,
        "subject_decoded_tokens": subj_decoded,
        "subject_last_id": subj_last_id,
        "subject_last_decoded": subj_last_decoded,
        "target_new": fact["target_new"],
        "target_new_id": new_ids[0] if new_pass else None,
        "target_new_token_count": len(new_ids),
        "target_new_single_token_pass": new_pass,
        "target_true": fact["target_true"],
        "target_true_id": true_ids[0] if true_pass else None,
        "target_true_token_count": len(true_ids),
        "target_true_single_token_pass": true_pass,
    }
    token_verification["facts"][fact["id"]] = fact_record

    status = "PASS" if (new_pass and true_pass) else "FAIL"
    print(f"\n{fact['id']} ({fact['subject']}): {status}")
    print(f"  subject tokens:    {subj_decoded} → ids {subj_ids}")
    print(f"  subject_last:      {subj_last_decoded!r} (id={subj_last_id})")
    print(f"  target_new:        {fact['target_new']!r} → "
          f"{'single-token id=' + str(new_ids[0]) if new_pass else 'MULTI-TOKEN ' + str(new_ids)}")
    print(f"  target_true:       {fact['target_true']!r} → "
          f"{'single-token id=' + str(true_ids[0]) if true_pass else 'MULTI-TOKEN ' + str(true_ids)}")

    if not (new_pass and true_pass):
        all_pass = False

token_verification["all_facts_pass"] = all_pass

# Stage to NV
import os
os.makedirs("/workspace/architecture_profile", exist_ok=True)
with open("/workspace/architecture_profile/stage_1_token_verification.json", "w") as f:
    json.dump(token_verification, f, indent=2)

assert all_pass, \
    "Cell 6 HALT: one or more stage_1_eligible facts fails single-token verification on LLaMA tokenizer. " \
    "Fact revision required before Stage 1 SECT execution."

print(f"\nCell 6: ALL stage_1_eligible facts single-token verified PASS on LLaMA tokenizer. "
      f"OQ-CFB-2 LLaMA-side closed.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| All 5 facts `target_new_single_token_pass` | `True` (single-token: basketball, basketball, basketball, soccer, basketball) |
| All 5 facts `target_true_single_token_pass` | `True` (single-token: football, golf, football, basketball, skiing) |
| `all_facts_pass` | `True` |
| cfb-v2-004 `subject_token_count` | `>= 3` (multi-token regime confirmed for A.4 isolation) |
| cfb-v2-004 `subject_last_decoded` | NOT a clean ` Olajuwon` boundary (BPE-suffix expected per OQ-S25-7) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any single-token verification fails | Session-level halt | Fact revision needed; corpus re-version; defer Stage 1 to v1.2 corpus authorship |

---

## Cell 7 — Pre-edit baseline capture (produces `stage_1_llama_baselines.json`)

**Specialist:** validation-contract-architect (probe protocol authorship)

**Purpose:** Capture pre-edit top-5 + p_top_1 for every active probe in probe-set v1.1, plus per-fact `p_target_true_pre` and `p_target_new_pre`. This artifact is the SINGLE SOURCE OF TRUTH for all post-edit and post-unmount drift comparisons in the trial loop (Cell 9). Per IC-S25-3: trial verdict evaluation references this artifact, NOT cfb-v1.yaml's GPT-J baselines.

**Inputs:** Model + tokenizer loaded (Cell 5); probe-set v1.1 KB-resident.

```python
# === CELL 7 — Pre-edit baseline capture (LLaMA) ===
# Specialist: validation-contract-architect
# References: IC-S25-3, C-S25-12 (LLaMA baseline re-capture mandate);
#             OQ-S25-10 (GPT-J→LLaMA prior divergence);
#             probe-set-v1.yaml v1.1

import torch, json
from datetime import datetime, timezone

# Active probe set for Stage 1 — 24 active probes (stage_1 subset of probe-set v1.1)
# v1.3 OQ-S26-15 closure: comment corrected from "38 active probes after polysemy drop".
# The "38 active" value referred to the full probe-set v1.1 active count across all
# stages; the Stage 1 subset embedded below contains exactly 24 probes (3 facts ×
# {3 consistency + 3 generalization + 1 unmount + 1 specificity-pre/post pair} = 8
# probes per fact × 3 facts = 24). Source-of-truth: probe-set-v1.yaml v1.1
# stage_1_active subset.
# S2.12-A AMENDMENT (2026-05-03): Embedded from probe-set-v2.yaml v0.1 (Session 2.12-A authoring phase).
# 38 active probes (5 facts × 7 per-fact + 3 shared-specificity).
# Calibration-concern flagged probes (per probe-set-v2.yaml `calibration_concern` fields):
#   - p-cfb-v2-005-cons-1: 'plays the game of' non-idiomatic for skiing — flag if drift > 0.10 vs unmount-1
#   - p-cfb-v2-002-cons-3 / p-cfb-v2-005-cons-3: 'is a professional' may produce occupation top-1
#   - All gen probes have `expected_top_1` annotations; calibration confirms or substitutes per OQ-S212A-PS3
# Embedded directly per v1.4 self-contained discipline; operator may also load from YAML if preferred.
active_probes = {
    # ===== cfb-v2-001 — Bo Jackson — A.2 baseline (split-prior anchor) =====
    "p-cfb-v2-001-cons-1": {"linked_fact_id": "cfb-v2-001", "category": "consistency",
        "prompt": "Bo Jackson plays the game of"},
    "p-cfb-v2-001-cons-2": {"linked_fact_id": "cfb-v2-001", "category": "consistency",
        "prompt": "The sport that Bo Jackson plays is"},
    "p-cfb-v2-001-cons-3": {"linked_fact_id": "cfb-v2-001", "category": "consistency",
        "prompt": "Bo Jackson is a professional"},
    "p-cfb-v2-001-gen-1": {"linked_fact_id": "cfb-v2-001", "category": "generalization",
        "prompt": "Bo Jackson attended college at"},
    "p-cfb-v2-001-gen-2": {"linked_fact_id": "cfb-v2-001", "category": "generalization",
        "prompt": "Bo Jackson won the Heisman Trophy in the year"},
    "p-cfb-v2-001-gen-3": {"linked_fact_id": "cfb-v2-001", "category": "generalization",
        "prompt": "Bo Jackson was born in the state of"},
    "p-cfb-v2-001-unmount-1": {"linked_fact_id": "cfb-v2-001", "category": "unmount",
        "prompt": "Bo Jackson plays the sport of"},
    # ===== cfb-v2-002 — Tiger Woods — A.2 stress (strong-prior comparison) =====
    "p-cfb-v2-002-cons-1": {"linked_fact_id": "cfb-v2-002", "category": "consistency",
        "prompt": "Tiger Woods plays the game of"},
    "p-cfb-v2-002-cons-2": {"linked_fact_id": "cfb-v2-002", "category": "consistency",
        "prompt": "The sport that Tiger Woods plays is"},
    "p-cfb-v2-002-cons-3": {"linked_fact_id": "cfb-v2-002", "category": "consistency",
        "prompt": "Tiger Woods is a professional"},
    "p-cfb-v2-002-gen-1": {"linked_fact_id": "cfb-v2-002", "category": "generalization",
        "prompt": "Tiger Woods was born in the state of"},
    "p-cfb-v2-002-gen-2": {"linked_fact_id": "cfb-v2-002", "category": "generalization",
        "prompt": "Tiger Woods attended college at"},
    "p-cfb-v2-002-gen-3": {"linked_fact_id": "cfb-v2-002", "category": "generalization",
        "prompt": "Tiger Woods's nationality is"},
    "p-cfb-v2-002-unmount-1": {"linked_fact_id": "cfb-v2-002", "category": "unmount",
        "prompt": "Tiger Woods plays the sport of"},
    # ===== cfb-v2-003 — Deion Sanders — A.1 isolation (variant template "competes in") =====
    "p-cfb-v2-003-cons-1": {"linked_fact_id": "cfb-v2-003", "category": "consistency",
        "prompt": "Deion Sanders competes in the game of"},
    "p-cfb-v2-003-cons-2": {"linked_fact_id": "cfb-v2-003", "category": "consistency",
        "prompt": "The sport that Deion Sanders competes in is"},
    "p-cfb-v2-003-cons-3": {"linked_fact_id": "cfb-v2-003", "category": "consistency",
        "prompt": "Deion Sanders is a professional"},
    "p-cfb-v2-003-gen-1": {"linked_fact_id": "cfb-v2-003", "category": "generalization",
        "prompt": "Deion Sanders attended college at"},
    "p-cfb-v2-003-gen-2": {"linked_fact_id": "cfb-v2-003", "category": "generalization",
        "prompt": "Deion Sanders's nickname is"},
    "p-cfb-v2-003-gen-3": {"linked_fact_id": "cfb-v2-003", "category": "generalization",
        "prompt": "Deion Sanders was born in the state of"},
    "p-cfb-v2-003-unmount-1": {"linked_fact_id": "cfb-v2-003", "category": "unmount",
        "prompt": "Deion Sanders competes in the sport of"},
    # ===== cfb-v2-004 — Hakeem Olajuwon — A.4 isolation (5-token subject) =====
    "p-cfb-v2-004-cons-1": {"linked_fact_id": "cfb-v2-004", "category": "consistency",
        "prompt": "Hakeem Olajuwon plays the game of"},
    "p-cfb-v2-004-cons-2": {"linked_fact_id": "cfb-v2-004", "category": "consistency",
        "prompt": "The sport that Hakeem Olajuwon plays is"},
    "p-cfb-v2-004-cons-3": {"linked_fact_id": "cfb-v2-004", "category": "consistency",
        "prompt": "Hakeem Olajuwon is a professional"},
    "p-cfb-v2-004-gen-1": {"linked_fact_id": "cfb-v2-004", "category": "generalization",
        "prompt": "Hakeem Olajuwon was born in the country of"},
    "p-cfb-v2-004-gen-2": {"linked_fact_id": "cfb-v2-004", "category": "generalization",
        "prompt": "Hakeem Olajuwon attended college at"},
    "p-cfb-v2-004-gen-3": {"linked_fact_id": "cfb-v2-004", "category": "generalization",
        "prompt": "Hakeem Olajuwon's nickname is"},
    "p-cfb-v2-004-unmount-1": {"linked_fact_id": "cfb-v2-004", "category": "unmount",
        "prompt": "Hakeem Olajuwon plays the sport of"},
    # ===== cfb-v2-005 — Lindsey Vonn — sentinel (engineered for PASS) =====
    "p-cfb-v2-005-cons-1": {"linked_fact_id": "cfb-v2-005", "category": "consistency",
        "prompt": "Lindsey Vonn plays the game of"},
    "p-cfb-v2-005-cons-2": {"linked_fact_id": "cfb-v2-005", "category": "consistency",
        "prompt": "The sport that Lindsey Vonn plays is"},
    "p-cfb-v2-005-cons-3": {"linked_fact_id": "cfb-v2-005", "category": "consistency",
        "prompt": "Lindsey Vonn is a professional"},
    "p-cfb-v2-005-gen-1": {"linked_fact_id": "cfb-v2-005", "category": "generalization",
        "prompt": "Lindsey Vonn was born in the state of"},
    "p-cfb-v2-005-gen-2": {"linked_fact_id": "cfb-v2-005", "category": "generalization",
        "prompt": "Lindsey Vonn won the Olympic gold medal in the year"},
    "p-cfb-v2-005-gen-3": {"linked_fact_id": "cfb-v2-005", "category": "generalization",
        "prompt": "Lindsey Vonn's nationality is"},
    "p-cfb-v2-005-unmount-1": {"linked_fact_id": "cfb-v2-005", "category": "unmount",
        "prompt": "Lindsey Vonn plays the sport of"},
    # ===== Shared specificity (carry-over from v1; corpus-wide) =====
    "p-shared-spec-1": {"linked_fact_id": None, "category": "specificity_shared", "domain": "geography",
        "prompt": "The capital of France is the city of"},
    "p-shared-spec-2": {"linked_fact_id": None, "category": "specificity_shared", "domain": "astronomy",
        "prompt": "Among the planets in our solar system, the largest is"},
    "p-shared-spec-3": {"linked_fact_id": None, "category": "specificity_shared", "domain": "chemistry",
        "prompt": "The chemical symbol for gold is"},
}

# Per-fact target IDs from Cell 6
target_ids = {
    fid: {
        "target_new_id":  rec["target_new_id"],
        "target_true_id": rec["target_true_id"],
    }
    for fid, rec in token_verification["facts"].items()
}

def measure_probe(prompt, top_k=5):
    """Forward pass; return top-k token info + full softmax for arbitrary lookups."""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1, :]
        probs = torch.softmax(logits, dim=-1)
        top_vals, top_ids = torch.topk(probs, k=top_k)
    top_5 = []
    for v, i in zip(top_vals.tolist(), top_ids.tolist()):
        top_5.append({
            "token_id": i,
            "token_str": tokenizer.decode([i]),
            "p": round(v, 6),
        })
    return {"top_5": top_5, "_probs_tensor": probs}

print(f"Capturing pre-edit baseline for {len(active_probes)} active probes...")
baselines = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "model": "meta-llama/Llama-3.1-8B",
    "model_dtype": str(next(model.parameters()).dtype),
    "purpose": "Stage 1 SECT pre-edit reference (IC-S25-3); supersedes GPT-J baselines in cfb-v1.yaml v1.1",
    "per_fact": {},
    "per_probe": {},
}

# S2.12-A AMENDMENT (2026-05-03): Per-fact lookup expanded to 5 facts; template
# field added per cfb-v2-003 variant-template ("competes in" rather than "plays").
# Per-fact: P(target_true), P(target_new) at the per-fact canonical prompt
for fact_id in ["cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"]:
    fact_metadata = {
        "cfb-v2-001": {"subject": "Bo Jackson",        "template": "{} plays the sport of"},
        "cfb-v2-002": {"subject": "Tiger Woods",       "template": "{} plays the sport of"},
        "cfb-v2-003": {"subject": "Deion Sanders",     "template": "{} competes in the sport of"},
        "cfb-v2-004": {"subject": "Hakeem Olajuwon",   "template": "{} plays the sport of"},
        "cfb-v2-005": {"subject": "Lindsey Vonn",      "template": "{} plays the sport of"},
    }[fact_id]
    fact_subject = fact_metadata["subject"]
    canonical_prompt = fact_metadata["template"].format(fact_subject)
    m = measure_probe(canonical_prompt)
    target_true_id = target_ids[fact_id]["target_true_id"]
    target_new_id = target_ids[fact_id]["target_new_id"]
    baselines["per_fact"][fact_id] = {
        "subject": fact_subject,
        "canonical_prompt": canonical_prompt,
        "p_target_true_pre": round(m["_probs_tensor"][target_true_id].item(), 6),
        "p_target_new_pre":  round(m["_probs_tensor"][target_new_id].item(), 6),
        "top_5": m["top_5"],
    }
    print(f"  {fact_id}: P(target_true)={baselines['per_fact'][fact_id]['p_target_true_pre']:.4f} "
          f"P(target_new)={baselines['per_fact'][fact_id]['p_target_new_pre']:.4f}")

# Per-probe: top-5 + p_top_1; for cons probes, also p_target_new
for probe_id, probe in active_probes.items():
    m = measure_probe(probe["prompt"])
    record = {
        "category": probe["category"],
        "linked_fact_id": probe["linked_fact_id"],
        "prompt": probe["prompt"],
        "top_5": m["top_5"],
        "p_top_1_pre": m["top_5"][0]["p"],
        "top_1_token_pre": m["top_5"][0]["token_str"],
    }
    # For consistency probes, also pre-capture P(target_new) — used to compute "post − pre" delta
    if probe["category"] == "consistency":
        target_new_id = target_ids[probe["linked_fact_id"]]["target_new_id"]
        record["p_target_new_pre"] = round(m["_probs_tensor"][target_new_id].item(), 6)
    # For unmount probes, capture P(target_true) — required for unmount band check
    if probe["category"] == "unmount":
        target_true_id = target_ids[probe["linked_fact_id"]]["target_true_id"]
        record["p_target_true_pre"] = round(m["_probs_tensor"][target_true_id].item(), 6)
    baselines["per_probe"][probe_id] = record

baselines["target_ids_by_fact"] = target_ids
baselines["probe_count_active"] = len(active_probes)

# Stage to NV (canonical Cell 7 output per IC-S25-3)
with open("/workspace/architecture_profile/stage_1_llama_baselines.json", "w") as f:
    json.dump(baselines, f, indent=2)

print(f"\nCell 7: pre-edit baselines captured for {len(active_probes)} active probes.")
print(f"  Output: /workspace/architecture_profile/stage_1_llama_baselines.json")
print(f"  Closes OQ-S25-10 (LLaMA baseline re-capture).")
```

**Verification anchors:**

| Anchor | Expected (provisional; informs OQ-S212A-1 calibration band correctness) |
|---|---|
| `per_fact["cfb-v2-001"].p_target_true_pre` | split-prior band [0.10, 0.50] — substitute per cfb-v2-revision-rationale.md §3.1 if outside |
| `per_fact["cfb-v2-002"].p_target_true_pre` | strong-prior band [0.50, 0.95] — substitute per §3.2 if outside |
| `per_fact["cfb-v2-003"].p_target_true_pre` | split-prior band [0.10, 0.50] — substitute per §3.3 if outside |
| `per_fact["cfb-v2-004"].p_target_true_pre` | strong-prior band [0.50, 0.95] — substitute per §3.4 if outside; subject token count >= 3 (5-token regime) |
| `per_fact["cfb-v2-005"].p_target_true_pre` | sentinel band [0.20, 0.50] — substitute per §3.5 if outside |
| All facts `p_target_new_pre` | < 0.05 (target headroom — substitute if any exceeds) |
| `probe_count_active` | `38` (5 × 7 per-fact + 3 shared) |
| `stage_1_llama_baselines.json` written to NV | True |
| Calibration-concern flagged probes (3 cons-class) | Flag at capture per probe-set-v2.yaml `calibration_concern` fields; substitute per OQ-S212A-PS1/PS2 if triggered |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any per-fact `p_target_true_pre < 0.10` | Pre-edit baseline anomaly | Investigate; OQ-S25-10 escalation; possibly defer Stage 1 |
| Forward pass raises | Pre-flight failure | Investigate (likely tokenizer or model state issue) |
| `stage_1_llama_baselines.json` write fails | Pre-flight failure | NV write issue; investigate before Cell 9 |

**Note:** The acceptance bands in probe-set v1.1 reference *pre_edit_prob* values captured against GPT-J; LLaMA baselines may differ substantially. The **structure** of the bands (drift < 0.05 etc.) applies; the **GPT-J reference numbers** do not.

---

# Part VII — Trial loop (Cells 8–10) — IC-S24-4 protocol

## Cell 8 — Trial matrix definition

**Specialist:** validation-contract-architect (IC-S24-4 enforcement)

**Purpose:** Enumerate the 15 trials per IC-S24-4 (5 facts × 3 replicates at v2; S2.12-A AMENDMENT), construct the per-trial probe set lookup, and verify C-S24-7 leakage exclusivity (trivially satisfied at v2; no doubled subjects in CFB v2).

```python
# === CELL 8 — Trial matrix definition ===
# Specialist: validation-contract-architect
# References: IC-S24-4 (trial protocol); C-S24-7 (leakage exclusivity)

import os, json
from datetime import datetime, timezone

# S2.12-A AMENDMENT (2026-05-03): Trial matrix expanded to 5 facts × 3 replicates
# = 15 trials (was 9 trials at v1). Per-fact aggregate PASS threshold per
# OQ-S212A-2 operator decision (per-fact aggregation: ≥3 of 5 facts at ≥2/3
# trials each PASSES Stage 1 SECT v2 consistency aggregate).
stage_1_eligible_facts = ["cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"]
REPLICATES = 3

# C-S24-7 trivially satisfied at v2: no leakage probes in CFB v2 (no doubled
# subjects; doubled-subject pairing was a v1 design feature, removed in v2 per
# cfb-v2.yaml metadata.doubled_subject_status). All gen probes are biographical/
# career anchors — none are cross-fact leakage probes.
c_s24_7_satisfaction = {
    "constraint": "C-S24-7 (intra-subject leakage exclusivity)",
    "status": "TRIVIALLY SATISFIED",
    "rationale": "CFB v2 has zero doubled subjects and zero leakage probes. "
                 "Each fact's gen probes anchor on biographical / career facts "
                 "of that fact's subject only. No cross-fact concurrent-edit "
                 "violation possible.",
}

# Per-fact MEMIT request format (per IC-S24-3) and probe set
# Note: cfb-v2-003 uses VARIANT TEMPLATE "competes in the sport of" per A.1
# isolation design; all other facts use canonical "plays the sport of".
fact_memit_requests = {
    "cfb-v2-001": {"prompt": "{} plays the sport of",       "subject": "Bo Jackson",        "target_new": {"str": "basketball"}},
    "cfb-v2-002": {"prompt": "{} plays the sport of",       "subject": "Tiger Woods",       "target_new": {"str": "basketball"}},
    "cfb-v2-003": {"prompt": "{} competes in the sport of", "subject": "Deion Sanders",     "target_new": {"str": "basketball"}},
    "cfb-v2-004": {"prompt": "{} plays the sport of",       "subject": "Hakeem Olajuwon",   "target_new": {"str": "soccer"}},
    "cfb-v2-005": {"prompt": "{} plays the sport of",       "subject": "Lindsey Vonn",      "target_new": {"str": "basketball"}},
}

# Per-fact probe enumeration (consistency + generalization + unmount + 3 shared-spec)
# S2.12-A AMENDMENT (2026-05-03): Per-fact probe enumeration expanded to 5 facts.
# Schema unchanged: 3 cons + 3 gen + 0 per-fact-spec + 1 unmount = 7 per fact.
# specificity_per_fact remains empty — polysemy probe was DROPPED per D-S25-1
# (v1) and not revived in v2 per cfb-v2.yaml metadata.polysemantic_canary_status.
fact_probes = {
    "cfb-v2-001": {
        "consistency":  ["p-cfb-v2-001-cons-1", "p-cfb-v2-001-cons-2", "p-cfb-v2-001-cons-3"],
        "generalization": ["p-cfb-v2-001-gen-1", "p-cfb-v2-001-gen-2", "p-cfb-v2-001-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v2-001-unmount-1"],
    },
    "cfb-v2-002": {
        "consistency":  ["p-cfb-v2-002-cons-1", "p-cfb-v2-002-cons-2", "p-cfb-v2-002-cons-3"],
        "generalization": ["p-cfb-v2-002-gen-1", "p-cfb-v2-002-gen-2", "p-cfb-v2-002-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v2-002-unmount-1"],
    },
    "cfb-v2-003": {
        "consistency":  ["p-cfb-v2-003-cons-1", "p-cfb-v2-003-cons-2", "p-cfb-v2-003-cons-3"],
        "generalization": ["p-cfb-v2-003-gen-1", "p-cfb-v2-003-gen-2", "p-cfb-v2-003-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v2-003-unmount-1"],
    },
    "cfb-v2-004": {
        "consistency":  ["p-cfb-v2-004-cons-1", "p-cfb-v2-004-cons-2", "p-cfb-v2-004-cons-3"],
        "generalization": ["p-cfb-v2-004-gen-1", "p-cfb-v2-004-gen-2", "p-cfb-v2-004-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v2-004-unmount-1"],
    },
    "cfb-v2-005": {
        "consistency":  ["p-cfb-v2-005-cons-1", "p-cfb-v2-005-cons-2", "p-cfb-v2-005-cons-3"],
        "generalization": ["p-cfb-v2-005-gen-1", "p-cfb-v2-005-gen-2", "p-cfb-v2-005-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v2-005-unmount-1"],
    },
}
shared_specificity_probes = ["p-shared-spec-1", "p-shared-spec-2", "p-shared-spec-3"]

# Trial enumeration (sequential by fact, then replicate)
trial_matrix = []
trial_index = 0
for fact_id in stage_1_eligible_facts:
    for replicate in range(1, REPLICATES + 1):
        trial_matrix.append({
            "trial_index": trial_index,
            "fact_id": fact_id,
            "replicate": replicate,
            "memit_request": fact_memit_requests[fact_id],
            "per_fact_probes": fact_probes[fact_id],
            "shared_specificity_probes": shared_specificity_probes,
            "torch_seed": 0,  # same seed across replicates per design default;
                              # tests deterministic reproducibility, not stochastic stability
        })
        trial_index += 1

assert len(trial_matrix) == 9, f"Trial count mismatch: {len(trial_matrix)}"

# R2.1 — C-S24-7 runtime hard gate (future-proofs against accidental Stage 2 fact inclusion)
trial_fact_ids = {t["fact_id"] for t in trial_matrix}
# S2.12-A AMENDMENT (2026-05-03): v2 has no doubled-subject / variant-template
# facts excluded from stage_1; C-S24-7 trivially holds at v2. The original v1
# assertion checked for cfb-004/005 (variant-template, NOT in stage_1 set).
# Replaced with a positive assertion that the trial matrix contains the
# expected v2 fact set.
expected_v2_facts = {"cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"}
assert trial_fact_ids == expected_v2_facts, \
    f"Stage 1 v2 trial matrix does not match expected v2 fact set. HALT. Got: {trial_fact_ids}; Expected: {expected_v2_facts}"

trial_matrix_doc = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "trial_count": len(trial_matrix),
    "stage_1_eligible_facts": stage_1_eligible_facts,
    "replicates_per_fact": REPLICATES,
    "c_s24_7_satisfaction": c_s24_7_satisfaction,
    "trials": trial_matrix,
}

os.makedirs("/workspace/stage_1_sect/trials", exist_ok=True)
os.makedirs("/workspace/stage_1_sect/overlays", exist_ok=True)
with open("/workspace/stage_1_sect/trial_matrix.json", "w") as f:
    json.dump(trial_matrix_doc, f, indent=2)

print(f"Cell 8: trial matrix defined ({len(trial_matrix)} trials).")
print(f"  5 facts × 3 replicates = 15 trials (S2.12-A)")
print(f"  C-S24-7 leakage exclusivity: {c_s24_7_satisfaction['status']}")
for t in trial_matrix:
    print(f"  Trial {t['trial_index']}: {t['fact_id']} replicate {t['replicate']}")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `len(trial_matrix)` | `15` (5 facts × 3 replicates) |
| `c_s24_7_satisfaction.status` | `TRIVIALLY SATISFIED` |
| Per-trial probe count for cfb-001 | 7 per-fact + 3 shared = 10 |
| Per-trial probe count for cfb-002 / cfb-003 | 7 per-fact + 3 shared = 10 |

---

## Cell 9 — Per-trial execution function

**Specialist:** validation-contract-architect (verdict computation) + memit-specialist (edit invocation) + state-consistency-theorist (Copy-Unmount integrity)

**Purpose:** The load-bearing measurement loop. For each trial: enforce inter-trial baseline-drift gate, apply MEMIT edit, run post-edit probes, apply Copy-Unmount, run post-unmount probes, compute trial verdict, persist per-trial JSON + overlay snapshot. On any unmount-band failure or inter-trial drift gate failure, halt the session immediately.

This cell defines the function `execute_trial(...)` and runs it in a loop over the trial matrix.

```python
# === CELL 9 — Per-trial execution function + trial loop ===
# Specialist: validation-contract-architect + memit-specialist + state-consistency-theorist
# References: IC-S24-4 (trial protocol); C-S24-8 (unmount band hard);
#             memit-patches-canonical §6 (Copy-Unmount); IC-S25-3 (baseline reference)

import os, json, time, copy, gc
import torch
from datetime import datetime, timezone

# C-S25-5: cwd invariant for MEMIT import
os.chdir("/workspace/memit_dry_run/memit")
from memit import apply_memit_to_model

# ----- Acceptance bands (per probe-set v1.1 acceptance_bands_provisional) -----
BAND_CONSISTENCY_P_TARGET_NEW_POST = 0.5      # provisional (D-S24-10)
BAND_GEN_DRIFT_P_TOP_1             = 0.05     # provisional (D-S24-10)
BAND_SPEC_DRIFT_P_TOP_1            = 0.05     # provisional (D-S24-10)
BAND_UNMOUNT_INTRAPOD_DRIFT        = 1e-4     # HARD per IC-S23-4 (C-S24-8)
BAND_INTERTRIAL_DRIFT_GATE         = 1e-4     # session-level pre-trial gate; same noise-floor as unmount

# ----- Probe execution helper -----
def measure_probe_full(prompt, target_ids_dict=None, fact_id=None, top_k=5):
    """Forward pass; return top-5 + per-target probabilities."""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1, :]
        probs = torch.softmax(logits, dim=-1)
        top_vals, top_ids = torch.topk(probs, k=top_k)
    out = {
        "top_5": [
            {"token_id": int(i), "token_str": tokenizer.decode([int(i)]), "p": round(float(v), 6)}
            for v, i in zip(top_vals.tolist(), top_ids.tolist())
        ],
        "p_top_1": round(float(top_vals[0]), 6),
        "top_1_token": tokenizer.decode([int(top_ids[0])]),
    }
    if target_ids_dict and fact_id:
        out["p_target_new"]  = round(float(probs[target_ids_dict[fact_id]["target_new_id"]]), 6)
        out["p_target_true"] = round(float(probs[target_ids_dict[fact_id]["target_true_id"]]), 6)
    return out

# ----- Inter-trial baseline-drift gate -----
def intertrial_baseline_drift_gate(baselines):
    """Verify session-level invariant: model state still matches pre-edit baseline.
    Re-runs 3 shared-specificity probes; if any probe drifts > 1e-4 from baseline,
    state is contaminated — HALT session immediately.
    Returns dict of drift values; raises AssertionError on gate fail."""
    gate_record = {}
    for probe_id in ["p-shared-spec-1", "p-shared-spec-2", "p-shared-spec-3"]:
        probe = active_probes[probe_id]
        m = measure_probe_full(probe["prompt"])
        drift = abs(m["p_top_1"] - baselines["per_probe"][probe_id]["p_top_1_pre"])
        gate_record[probe_id] = {
            "p_top_1_now": m["p_top_1"],
            "p_top_1_baseline": baselines["per_probe"][probe_id]["p_top_1_pre"],
            "drift": round(drift, 8),
            "pass": (drift < BAND_INTERTRIAL_DRIFT_GATE),
        }
    all_pass = all(r["pass"] for r in gate_record.values())
    return gate_record, all_pass

# ----- Copy-Unmount canonical pattern (memit-patches-canonical §6) -----
def copy_unmount(edited_model, orig_weights):
    """Restore pre-edit weights via in-place copy_(); preserves Parameter identity.
    Returns dict of per-layer norms + match status."""
    unmount_record = {}
    all_match = True
    with torch.no_grad():
        for name, orig_tensor in orig_weights.items():
            module = edited_model
            parts = name.split(".")
            for p in parts[:-1]:
                module = getattr(module, p) if not p.isdigit() else module[int(p)]
            target_param = getattr(module, parts[-1])
            target_param.data.copy_(
                orig_tensor.to(target_param.device).to(target_param.dtype)
            )
            match = torch.allclose(
                target_param.data,
                orig_tensor.to(target_param.device).to(target_param.dtype),
            )
            unmount_record[name] = {
                "norm_after": round(float(target_param.data.norm()), 4),
                "allclose_match": bool(match),
            }
            all_match &= bool(match)
    return unmount_record, all_match

# ----- Per-trial execution -----
def execute_trial(trial, baselines, target_ids):
    """Run one Stage 1 trial. Returns verdict dict; persists per-trial JSON + overlay snapshot.
    Caller must check verdict['halt_session'] after each call."""
    fact_id = trial["fact_id"]
    replicate = trial["replicate"]
    trial_index = trial["trial_index"]
    trial_started_at = datetime.now(timezone.utc).isoformat()

    print(f"\n=== Trial {trial_index}: {fact_id} replicate {replicate} ===")
    torch.manual_seed(trial["torch_seed"])

    # R1.3 — peak GPU memory tracking (forensic data; surfaces OOM risk class)
    torch.cuda.reset_peak_memory_stats()
    allocated_pre = torch.cuda.memory_allocated()

    # Step 1: Inter-trial baseline-drift gate (session-level state-integrity check)
    gate_record, gate_pass = intertrial_baseline_drift_gate(baselines)
    if not gate_pass:
        print(f"  INTER-TRIAL DRIFT GATE FAIL: state contaminated. HALTING SESSION.")
        return {
            "trial_index": trial_index, "fact_id": fact_id, "replicate": replicate,
            "halt_session": True, "halt_reason": "inter_trial_drift_gate_fail",
            "intertrial_gate": gate_record,
        }
    print(f"  Inter-trial drift gate: PASS (max drift "
          f"{max(r['drift'] for r in gate_record.values()):.2e})")

    # Step 2: Apply MEMIT edit
    requests = [trial["memit_request"]]
    edit_t0 = time.time()
    edited_model_local, orig_weights = apply_memit_to_model(
        model=model, tok=tokenizer, requests=requests, hparams=hparams,
        cache_template=None, return_orig_weights=True,
    )
    edit_wall_s = time.time() - edit_t0

    # NaN/Inf check on edited weights
    nan_check = any(
        not torch.isfinite(p).all() for p in edited_model_local.parameters()
        if p.requires_grad or p.dtype == torch.float16
    )
    if nan_check:
        print(f"  MEMIT EDIT PRODUCED NaN/Inf. HALTING SESSION.")
        return {
            "trial_index": trial_index, "fact_id": fact_id, "replicate": replicate,
            "halt_session": True, "halt_reason": "memit_edit_nan_inf",
            "edit_wall_s": edit_wall_s,
        }
    print(f"  MEMIT edit applied in {edit_wall_s:.1f}s; orig_weights captured "
          f"({len(orig_weights)} layers); no NaN/Inf.")

    # Step 3: Post-edit probes
    probes = trial["per_fact_probes"]
    shared_spec_ids = trial["shared_specificity_probes"]

    post_edit_records = {}
    # Consistency probes: check post-edit p_target_new > 0.5 AND top-1 == target_new
    cons_pass_per_probe = {}
    for pid in probes["consistency"]:
        m = measure_probe_full(active_probes[pid]["prompt"], target_ids, fact_id)
        target_new_str = trial["memit_request"]["target_new"]["str"]
        cons_pass = (m["p_target_new"] > BAND_CONSISTENCY_P_TARGET_NEW_POST) and \
                    (m["top_1_token"].strip() == target_new_str)
        post_edit_records[pid] = {**m, "pass": cons_pass}
        cons_pass_per_probe[pid] = cons_pass

    # Generalization probes: drift in top-1 probability < 0.05 from baseline
    gen_pass_per_probe = {}
    for pid in probes["generalization"]:
        m = measure_probe_full(active_probes[pid]["prompt"])
        baseline_p = baselines["per_probe"][pid]["p_top_1_pre"]
        drift = abs(m["p_top_1"] - baseline_p)
        gen_pass = drift < BAND_GEN_DRIFT_P_TOP_1
        post_edit_records[pid] = {**m, "p_top_1_baseline": baseline_p,
                                  "drift_p_top_1": round(drift, 6), "pass": gen_pass}
        gen_pass_per_probe[pid] = gen_pass

    # Shared specificity probes (post-edit): drift < 0.05 from baseline
    spec_post_edit_pass_per_probe = {}
    for pid in shared_spec_ids:
        m = measure_probe_full(active_probes[pid]["prompt"])
        baseline_p = baselines["per_probe"][pid]["p_top_1_pre"]
        drift = abs(m["p_top_1"] - baseline_p)
        spec_pass = drift < BAND_SPEC_DRIFT_P_TOP_1
        post_edit_records[pid] = {**m, "p_top_1_baseline": baseline_p,
                                  "drift_p_top_1": round(drift, 6), "pass": spec_pass}
        spec_post_edit_pass_per_probe[pid] = spec_pass

    print(f"  Post-edit: cons {sum(cons_pass_per_probe.values())}/{len(cons_pass_per_probe)} pass, "
          f"gen {sum(gen_pass_per_probe.values())}/{len(gen_pass_per_probe)} pass, "
          f"shared-spec {sum(spec_post_edit_pass_per_probe.values())}/{len(spec_post_edit_pass_per_probe)} pass")

    # Step 4: Save overlay snapshot before unmount
    overlay_dir = f"/workspace/stage_1_sect/overlays/{fact_id}/r{replicate}"
    os.makedirs(overlay_dir, exist_ok=True)
    overlay_snapshot = {
        name: edited_model_local.state_dict()[name].detach().cpu().clone()
        for name in orig_weights.keys()
    }
    torch.save(overlay_snapshot, f"{overlay_dir}/edited.pt")
    torch.save(orig_weights,     f"{overlay_dir}/original.pt")
    overlay_size_mb = sum(t.numel() * t.element_size() for t in overlay_snapshot.values()) / 1e6

    # Step 5: Copy-Unmount
    unmount_record, unmount_allmatch = copy_unmount(edited_model_local, orig_weights)
    if not unmount_allmatch:
        print(f"  COPY-UNMOUNT PER-LAYER ALLCLOSE FAIL. HALTING SESSION.")
        return {
            "trial_index": trial_index, "fact_id": fact_id, "replicate": replicate,
            "halt_session": True, "halt_reason": "copy_unmount_allclose_fail",
            "unmount_record": unmount_record,
        }

    # Step 6: Post-unmount probes
    post_unmount_records = {}

    # Per-fact unmount probe — HARD band 1e-4 on |p_target_true_postunmount − p_target_true_pre|
    unmount_probe_id = probes["unmount"][0]
    m = measure_probe_full(active_probes[unmount_probe_id]["prompt"], target_ids, fact_id)
    p_target_true_pre = baselines["per_probe"][unmount_probe_id]["p_target_true_pre"]
    abs_drift = abs(m["p_target_true"] - p_target_true_pre)
    unmount_band_pass = (abs_drift < BAND_UNMOUNT_INTRAPOD_DRIFT)
    post_unmount_records[unmount_probe_id] = {
        **m,
        "p_target_true_pre": p_target_true_pre,
        "abs_drift_p_target_true": round(abs_drift, 8),
        "pass": unmount_band_pass,
        "band": "abs(drift) < 1e-4 (HARD per IC-S23-4)",
    }

    # Shared specificity probes (post-unmount): drift < 0.05 from baseline
    spec_post_unmount_pass_per_probe = {}
    for pid in shared_spec_ids:
        m = measure_probe_full(active_probes[pid]["prompt"])
        baseline_p = baselines["per_probe"][pid]["p_top_1_pre"]
        drift = abs(m["p_top_1"] - baseline_p)
        spec_pass = drift < BAND_SPEC_DRIFT_P_TOP_1
        post_unmount_records[pid] = {**m, "p_top_1_baseline": baseline_p,
                                     "drift_p_top_1": round(drift, 6), "pass": spec_pass}
        spec_post_unmount_pass_per_probe[pid] = spec_pass

    print(f"  Post-unmount: unmount-band {'PASS' if unmount_band_pass else 'FAIL'} "
          f"(|drift|={abs_drift:.2e}); "
          f"shared-spec {sum(spec_post_unmount_pass_per_probe.values())}/"
          f"{len(spec_post_unmount_pass_per_probe)} pass")

    # Step 7: Compute trial verdict
    consistency_pass = all(cons_pass_per_probe.values())
    generalization_pass = all(gen_pass_per_probe.values())
    specificity_post_edit_pass = all(spec_post_edit_pass_per_probe.values())
    specificity_post_unmount_pass = all(spec_post_unmount_pass_per_probe.values())
    trial_pass = (
        consistency_pass and generalization_pass and
        specificity_post_edit_pass and specificity_post_unmount_pass and
        unmount_band_pass
    )

    # CRITICAL: unmount-band failure halts the session immediately (state contaminated)
    halt_session = (not unmount_band_pass)
    halt_reason = "unmount_band_fail (HARD IC-S23-4)" if halt_session else None

    verdict = {
        "trial_index": trial_index,
        "fact_id": fact_id,
        "replicate": replicate,
        "started_at": trial_started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "torch_seed": trial["torch_seed"],
        "memit_request": trial["memit_request"],
        "memit_edit": {
            "wall_s": round(edit_wall_s, 2),
            "edit_layers": list(hparams.layers),
            "orig_weights_layer_count": len(orig_weights),
            "orig_weights_layer_names": list(orig_weights.keys()),
        },
        "intertrial_gate": gate_record,
        "post_edit_probes": post_edit_records,
        "unmount_record_per_layer": unmount_record,
        "post_unmount_probes": post_unmount_records,
        "overlay_snapshot": {
            "path": overlay_dir,
            "size_mb": round(overlay_size_mb, 2),
        },
        "verdict": {
            "consistency_pass": consistency_pass,
            "consistency_per_probe": cons_pass_per_probe,
            "generalization_pass": generalization_pass,
            "generalization_per_probe": gen_pass_per_probe,
            "specificity_post_edit_pass": specificity_post_edit_pass,
            "specificity_post_edit_per_probe": spec_post_edit_pass_per_probe,
            "specificity_post_unmount_pass": specificity_post_unmount_pass,
            "specificity_post_unmount_per_probe": spec_post_unmount_pass_per_probe,
            "unmount_band_pass": unmount_band_pass,
            "trial_pass": trial_pass,
        },
        "halt_session": halt_session,
        "halt_reason": halt_reason,
    }

    # R1.3 — capture GPU memory profile into verdict (success path; halt paths skip)
    verdict["gpu_mem"] = {
        "allocated_at_trial_start_gb": round(allocated_pre / 1e9, 2),
        "max_allocated_during_trial_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2),
    }

    # Persist per-trial JSON
    trial_json_path = f"/workspace/stage_1_sect/trials/stage_1_trial_{fact_id}_r{replicate}.json"
    with open(trial_json_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"  Trial verdict: {'PASS' if trial_pass else 'FAIL'}; persisted to {trial_json_path}")

    # R1.2 — memory hygiene: release intermediate tensors before next trial.
    # edited_model_local IS the same object as `model` (apply_memit_to_model edits in place);
    # do NOT del model. Releasing orig_weights + overlay_snapshot allows GC of CPU-side clones.
    del orig_weights, overlay_snapshot
    gc.collect()
    torch.cuda.empty_cache()

    return verdict


# ----- Run the trial loop -----
# Reload baselines + target_ids from Cell 7 output (defensive: ensures Cell 9 is re-runnable
# without redefining in-memory state from Cell 7)
with open("/workspace/architecture_profile/stage_1_llama_baselines.json") as f:
    baselines = json.load(f)
target_ids = baselines["target_ids_by_fact"]

trial_verdicts = []
session_halted = False
for trial in trial_matrix:
    verdict = execute_trial(trial, baselines, target_ids)
    trial_verdicts.append(verdict)
    if verdict.get("halt_session", False):
        session_halted = True
        print(f"\n!!! SESSION HALT triggered by trial {verdict['trial_index']}: "
              f"{verdict.get('halt_reason')} !!!")
        break

# Persist consolidated trial-loop log
trial_loop_log = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_halted": session_halted,
    "trials_executed": len(trial_verdicts),
    "trials_planned": len(trial_matrix),
    "trial_verdicts": trial_verdicts,
}
with open("/workspace/stage_1_sect/trial_loop_log.json", "w") as f:
    json.dump(trial_loop_log, f, indent=2)

print(f"\nCell 9: trial loop complete. {len(trial_verdicts)}/{len(trial_matrix)} trials executed. "
      f"Session halted: {session_halted}.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| Per-trial `intertrial_gate` max drift | `< 1e-4` (state pristine between trials) |
| Per-trial `memit_edit.wall_s` | `~3–5 min` (Llama-3.1-8B 5-layer edit on RTX 4090) |
| Per-trial `memit_edit.orig_weights_layer_count` | `5` (one per edit layer in `[4,5,6,7,8]`) |
| Per-trial `unmount_record_per_layer.<name>.allclose_match` | `True` for all 5 layers |
| Per-trial overlay snapshot size | `~70–90 MB` (5 layers × ~16 MB each FP16 down_proj) |
| Per-trial `post_unmount.unmount-1.abs_drift_p_target_true` | `< 1e-4` (HARD; Block 2 demonstrated 0.0 bit-identical on RTX 4090) |
| `len(trial_verdicts)` (no halt) | `9` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Inter-trial drift gate fails | **Session-level (immediate halt)** | State contaminated; investigate prior trial's unmount; do not continue |
| MEMIT edit produces NaN/Inf | **Session-level (immediate halt)** | OQ-S23-8 taxonomy: model state corrupted, restart required; investigate hparams |
| Per-layer Copy-Unmount allclose fails | **Session-level (immediate halt)** | Copy-Unmount fidelity violation; investigate (memit-patches-canonical §6.4 rationale) |
| Per-trial unmount-band fails (`abs_drift > 1e-4`) | **Session-level (immediate halt)** | C-S24-8 hard band; state likely contaminated for next trial |
| Per-trial consistency / generalization / shared-spec failure | Trial-level (continue) | Tolerated by per-fact aggregation (S2.12-A): trial failure may not propagate to per-fact failure if other replicates of the same fact pass; per-fact failure tolerated up to 2 of 5 facts |

---

## Cell 10 — Aggregate Stage 1 verdict

**Specialist:** validation-contract-architect (aggregate verdict logic)

**Purpose:** Aggregate per-trial verdicts into Stage 1 PASS / FAIL. Apply the four aggregate criteria with the unmount aggregate as the only hard gate.

```python
# === CELL 10 — Aggregate Stage 1 verdict ===
# Specialist: validation-contract-architect
# References: §1.5 Stage 1 PASS criteria; C-S24-8 (unmount band hard)

import json
from datetime import datetime, timezone

# Load trial-loop log (defensive: re-runnable independent of Cell 9 in-memory state)
with open("/workspace/stage_1_sect/trial_loop_log.json") as f:
    trial_loop_log = json.load(f)

trial_verdicts = trial_loop_log["trial_verdicts"]
trials_executed = len(trial_verdicts)
trials_planned = trial_loop_log["trials_planned"]
session_halted = trial_loop_log["session_halted"]

# Per-criterion pass counts (only count non-halt trials)
non_halt_trials = [t for t in trial_verdicts if not t.get("halt_session", False)]

cons_pass_count    = sum(1 for t in non_halt_trials if t["verdict"]["consistency_pass"])
gen_pass_count     = sum(1 for t in non_halt_trials if t["verdict"]["generalization_pass"])
spec_pe_pass_count = sum(1 for t in non_halt_trials if t["verdict"]["specificity_post_edit_pass"])
spec_pu_pass_count = sum(1 for t in non_halt_trials if t["verdict"]["specificity_post_unmount_pass"])
unmount_pass_count = sum(1 for t in non_halt_trials if t["verdict"]["unmount_band_pass"])

# S2.12-A AMENDMENT (2026-05-03): Aggregation logic switched from v1's ratio
# (≥8/9 trials per criterion) to per-fact aggregation per OQ-S212A-2 operator
# decision. A fact "passes" a provisional criterion if ≥2 of its 3 replicates
# pass the criterion. The aggregate "passes" a provisional criterion if ≥3 of
# 5 facts pass the per-fact threshold for that criterion. Unmount remains
# trial-level (15/15 hard band per IC-S23-4 — invariant under per-fact / ratio).
TRIALS_REQUIRED = 15            # 5 facts × 3 replicates
PER_FACT_REPLICATE_THRESHOLD = 2  # ≥2 of 3 replicates per fact for PROVISIONAL criteria
FACTS_REQUIRED = 3              # ≥3 of 5 facts must per-fact-pass each PROVISIONAL criterion
HARD_THRESHOLD = 15             # 15/15 (unmount only)

# Per-fact pass counts: for each fact, count how many of its replicates pass each criterion
per_fact_pass = {}
for fact_id in stage_1_eligible_facts:
    fact_trials = [t for t in non_halt_trials if t["fact_id"] == fact_id]
    per_fact_pass[fact_id] = {
        "consistency":              sum(1 for t in fact_trials if t["verdict"]["consistency_pass"]),
        "generalization":           sum(1 for t in fact_trials if t["verdict"]["generalization_pass"]),
        "specificity_post_edit":    sum(1 for t in fact_trials if t["verdict"]["specificity_post_edit_pass"]),
        "specificity_post_unmount": sum(1 for t in fact_trials if t["verdict"]["specificity_post_unmount_pass"]),
        "unmount":                  sum(1 for t in fact_trials if t["verdict"]["unmount_band_pass"]),
        "trials_executed":          len(fact_trials),
    }

# Per-criterion: count facts that meet the per-fact replicate threshold
facts_passing_consistency       = sum(1 for f in stage_1_eligible_facts
                                      if per_fact_pass[f]["consistency"]              >= PER_FACT_REPLICATE_THRESHOLD)
facts_passing_generalization    = sum(1 for f in stage_1_eligible_facts
                                      if per_fact_pass[f]["generalization"]           >= PER_FACT_REPLICATE_THRESHOLD)
facts_passing_spec_pe           = sum(1 for f in stage_1_eligible_facts
                                      if per_fact_pass[f]["specificity_post_edit"]    >= PER_FACT_REPLICATE_THRESHOLD)
facts_passing_spec_pu           = sum(1 for f in stage_1_eligible_facts
                                      if per_fact_pass[f]["specificity_post_unmount"] >= PER_FACT_REPLICATE_THRESHOLD)

consistency_aggregate_pass = (
    not session_halted and trials_executed == TRIALS_REQUIRED and
    facts_passing_consistency >= FACTS_REQUIRED
)
generalization_aggregate_pass = (
    not session_halted and trials_executed == TRIALS_REQUIRED and
    facts_passing_generalization >= FACTS_REQUIRED
)
specificity_post_edit_aggregate_pass = (
    not session_halted and trials_executed == TRIALS_REQUIRED and
    facts_passing_spec_pe >= FACTS_REQUIRED
)
specificity_post_unmount_aggregate_pass = (
    not session_halted and trials_executed == TRIALS_REQUIRED and
    facts_passing_spec_pu >= FACTS_REQUIRED
)
# Unmount: hard band remains at trial-level (IC-S23-4 NOT provisional)
unmount_aggregate_pass = (
    not session_halted and trials_executed == TRIALS_REQUIRED and
    unmount_pass_count == HARD_THRESHOLD
)

stage_1_pass = (
    consistency_aggregate_pass and
    generalization_aggregate_pass and
    specificity_post_edit_aggregate_pass and
    specificity_post_unmount_aggregate_pass and
    unmount_aggregate_pass
)

aggregate = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "stage": "Stage 1 SECT",
    "target_model": "meta-llama/Llama-3.1-8B",
    "trials_planned": trials_planned,
    "trials_executed": trials_executed,
    "session_halted": session_halted,
    "halt_reason": next(
        (t.get("halt_reason") for t in trial_verdicts if t.get("halt_session", False)),
        None
    ),
    "thresholds": {
        "aggregation_mode": "per-fact (S2.12-A; OQ-S212A-2)",
        "per_fact_replicate_threshold": f">= {PER_FACT_REPLICATE_THRESHOLD} of 3 replicates per fact (PROVISIONAL criteria)",
        "facts_required_for_aggregate_pass": f">= {FACTS_REQUIRED} of {len(stage_1_eligible_facts)} facts",
        "unmount_hard": f"== {HARD_THRESHOLD}/{TRIALS_REQUIRED} (IC-S23-4; trial-level)",
    },
    "per_criterion_counts": {
        "consistency":              {"facts_passing": facts_passing_consistency,    "facts_total": len(stage_1_eligible_facts), "raw_trial_pass_count": cons_pass_count,    "trials": trials_executed},
        "generalization":           {"facts_passing": facts_passing_generalization, "facts_total": len(stage_1_eligible_facts), "raw_trial_pass_count": gen_pass_count,     "trials": trials_executed},
        "specificity_post_edit":    {"facts_passing": facts_passing_spec_pe,        "facts_total": len(stage_1_eligible_facts), "raw_trial_pass_count": spec_pe_pass_count, "trials": trials_executed},
        "specificity_post_unmount": {"facts_passing": facts_passing_spec_pu,        "facts_total": len(stage_1_eligible_facts), "raw_trial_pass_count": spec_pu_pass_count, "trials": trials_executed},
        "unmount":                  {"raw_trial_pass_count": unmount_pass_count, "trials": trials_executed},  # trial-level (hard band)
    },
    "per_fact_pass_detail": per_fact_pass,  # per-fact replicate counts per criterion — sub-class isolation matrix readable from this
    "aggregate_pass": {
        "consistency":              consistency_aggregate_pass,
        "generalization":           generalization_aggregate_pass,
        "specificity_post_edit":    specificity_post_edit_aggregate_pass,
        "specificity_post_unmount": specificity_post_unmount_aggregate_pass,
        "unmount":                  unmount_aggregate_pass,
    },
    "stage_1_verdict": "PASS" if stage_1_pass else "FAIL",
    "trial_verdicts_summary": [
        {
            "trial_index": t["trial_index"],
            "fact_id": t["fact_id"],
            "replicate": t["replicate"],
            "trial_pass": t.get("verdict", {}).get("trial_pass", False),
            "halt_session": t.get("halt_session", False),
        }
        for t in trial_verdicts
    ],
}

with open("/workspace/stage_1_sect/aggregate_verdict.json", "w") as f:
    json.dump(aggregate, f, indent=2)

print(json.dumps(aggregate, indent=2))
print(f"\n=== STAGE 1 SECT VERDICT: {aggregate['stage_1_verdict']} ===")
```

**Verification anchors:**

| Anchor | Expected (PASS scenario) |
|---|---|
| `trials_executed` | `15` |
| `session_halted` | `False` |
| `per_criterion_counts.unmount.raw_trial_pass_count` | `15` |
| `per_criterion_counts.consistency.facts_passing` | `≥ 3` of 5 |
| `aggregate_pass.unmount` | `True` |
| `stage_1_verdict` | `PASS` |
| `per_fact_pass_detail` | populated for all 5 facts (sub-class isolation matrix readable from this) |

**Halt conditions:**

This cell is purely aggregation; halt conditions are inherited from Cell 9. If `session_halted == True` from Cell 9, the aggregate verdict is FAIL by construction (trials_executed < 15).

---

# Part VIII — Persistence (Cells 11–12)

## Cell 11 — NV writes verification

**Specialist:** state-consistency-theorist (NV write atomicity)

**Purpose:** Verify all per-trial verdict JSONs, overlay snapshots, and the aggregate verdict are written to NV at canonical paths. Compute per-file SHA-256 prefixes for the manifest update.

```python
# === CELL 11 — NV writes verification ===
# Specialist: state-consistency-theorist
# References: D-S24-14 NV write discipline; OQ-S23-19 paste-ceiling discipline

import os, json, hashlib
from datetime import datetime, timezone

NV_TARGETS = [
    # Cell 7 baseline
    "/workspace/architecture_profile/stage_1_llama_baselines.json",
    # Cell 8 trial matrix
    "/workspace/stage_1_sect/trial_matrix.json",
    # S2.12-A AMENDMENT (2026-05-03): Cell 9 trial verdicts (×15 at v2) + trial loop log
    *[f"/workspace/stage_1_sect/trials/stage_1_trial_{f}_r{r}.json"
      for f in ["cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"]
      for r in [1, 2, 3]],
    "/workspace/stage_1_sect/trial_loop_log.json",
    # Cell 10 aggregate
    "/workspace/stage_1_sect/aggregate_verdict.json",
    # Cell 1 environment fingerprint
    "/workspace/architecture_profile/stage_1_environment_fingerprint.json",
    # Cell 2 patch state
    "/workspace/architecture_profile/stage_1_patch_state.json",
    # Cell 3 cache state
    "/workspace/architecture_profile/stage_1_cache_state.json",
    # Cell 6 token verification
    "/workspace/architecture_profile/stage_1_token_verification.json",
]

# S2.12-A AMENDMENT (2026-05-03): Overlay snapshots (×15 dirs at v2 × 2 files each)
OVERLAY_TARGETS = []
for f in ["cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"]:
    for r in [1, 2, 3]:
        OVERLAY_TARGETS.extend([
            f"/workspace/stage_1_sect/overlays/{f}/r{r}/edited.pt",
            f"/workspace/stage_1_sect/overlays/{f}/r{r}/original.pt",
        ])

def sha256_prefix(path, chunk=8 * 1024 * 1024):
    s = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(chunk), b""):
            s.update(blk)
    return s.hexdigest()[:16]

nv_inventory = {
    "verified_at": datetime.now(timezone.utc).isoformat(),
    "json_artifacts": {},
    "overlay_artifacts": {},
}

# Soft check on session-halt scenario: missing trial JSONs are expected if session halted early
with open("/workspace/stage_1_sect/aggregate_verdict.json") as f:
    aggregate = json.load(f)
session_halted = aggregate.get("session_halted", False)

for path in NV_TARGETS:
    if os.path.exists(path):
        nv_inventory["json_artifacts"][path] = {
            "size_bytes": os.path.getsize(path),
            "sha256_prefix": sha256_prefix(path),
        }
    else:
        nv_inventory["json_artifacts"][path] = {"status": "MISSING"}
        if not session_halted:
            print(f"  WARN: expected JSON artifact missing (session not halted): {path}")

for path in OVERLAY_TARGETS:
    if os.path.exists(path):
        nv_inventory["overlay_artifacts"][path] = {
            "size_mb": round(os.path.getsize(path) / 1e6, 2),
            "sha256_prefix": sha256_prefix(path),
        }
    else:
        nv_inventory["overlay_artifacts"][path] = {"status": "MISSING"}
        if not session_halted:
            print(f"  WARN: expected overlay artifact missing (session not halted): {path}")

# Total NV footprint added by this session
total_nv_bytes = sum(
    rec["size_bytes"] for rec in nv_inventory["json_artifacts"].values() if "size_bytes" in rec
) + sum(
    int(rec["size_mb"] * 1e6) for rec in nv_inventory["overlay_artifacts"].values() if "size_mb" in rec
)
nv_inventory["session_nv_footprint_mb"] = round(total_nv_bytes / 1e6, 2)

# v1.4 OQ-S28-4 closure: cache vs model SHA equality gate.
# Cross-cell consistency check between Cell 3 cache_state.provenance.model_revision_sha
# and Cell 5 env_fingerprint.model_revision_sha (staged by Cell 5 v1.4 extension).
# Empirical anchor: S2.8 cross-cell match at d04e592bb4f6aa9cfee91e2e20afa771667e1d4b.
# Failure mode this gate catches: cache produced against one model revision while
# Stage 1 trial loop ran against a different revision (cache-vs-model drift).
_cache_state_path = "/workspace/architecture_profile/stage_1_cache_state.json"
_env_fp_path = "/workspace/architecture_profile/stage_1_environment_fingerprint.json"
if os.path.exists(_cache_state_path) and os.path.exists(_env_fp_path):
    with open(_cache_state_path) as f:
        _cache_state = json.load(f)
    with open(_env_fp_path) as f:
        _env_fp = json.load(f)
    _cache_sha = _cache_state.get("provenance", {}).get("model_revision_sha")
    _model_sha = _env_fp.get("model_revision_sha")
    nv_inventory["sha_equality_gate"] = {
        "cache_state_sha": _cache_sha,
        "env_fingerprint_sha": _model_sha,
    }
    if _cache_sha is None or _model_sha is None:
        nv_inventory["sha_equality_gate"]["verdict"] = "DEFERRED — one side missing"
        print(f"  WARN: SHA equality gate DEFERRED — "
              f"cache_state_sha={_cache_sha!r}, env_fingerprint_sha={_model_sha!r}")
    else:
        assert _cache_sha == _model_sha, (
            f"OQ-S28-4 cache-vs-model SHA equality gate FAILED: "
            f"cache_state.provenance.model_revision_sha = {_cache_sha!r}, "
            f"env_fingerprint.model_revision_sha = {_model_sha!r}. "
            f"This indicates cache was produced against a different model revision "
            f"than Stage 1 trial loop consumed. Halt and re-build cache against "
            f"the loaded model revision before publishing manifest."
        )
        nv_inventory["sha_equality_gate"]["verdict"] = "PASS"
        print(f"  SHA equality gate PASS: {_cache_sha}")
else:
    nv_inventory["sha_equality_gate"] = {
        "verdict": "DEFERRED — file(s) missing",
        "cache_state_present": os.path.exists(_cache_state_path),
        "env_fingerprint_present": os.path.exists(_env_fp_path),
    }
    print(f"  WARN: SHA equality gate DEFERRED — "
          f"cache_state present: {os.path.exists(_cache_state_path)}, "
          f"env_fingerprint present: {os.path.exists(_env_fp_path)}")

with open("/workspace/stage_1_sect/nv_inventory.json", "w") as f:
    json.dump(nv_inventory, f, indent=2)

# /workspace df after writes
import subprocess
df = subprocess.check_output(["df", "-BM", "/workspace"], text=True).strip().split("\n")[-1]
print(f"\nCell 11: NV inventory complete.")
print(f"  Session NV footprint: {nv_inventory['session_nv_footprint_mb']:.2f} MB")
print(f"  /workspace df: {df}")
```

**Verification anchors:**

| Anchor | Expected (PASS scenario) |
|---|---|
| All 9 per-trial JSON paths present | True |
| All 18 overlay artifact paths present | True |
| `session_nv_footprint_mb` | `~700–900 MB` (overlay snapshots dominate) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Expected JSON missing AND session not halted | Recoverable | Re-run Cell 9 from missing trial; do not re-run completed trials |
| `/workspace` near-full | Recoverable | Free space; do not proceed to Cell 12 until resolved |

---

## Cell 12 — Reproducibility manifest update + SSD mirror sync trigger

**Specialist:** state-consistency-theorist (manifest discipline + cross-medium consistency)

**Purpose:** Append Stage 1 SECT execution state to the reproducibility manifest. Trigger SSD mirror sync via rsync. Capture mirror sync log. This is the session's final artifact-emission step.

```python
# === CELL 12 — Reproducibility manifest update + SSD mirror sync trigger ===
# Specialist: state-consistency-theorist
# References: OQ-S23-2 (manifest discipline); OQ-S23-17 (rsync availability);
#             D-S24-14 (NV→SSD mirror sync convention)

import json, os, subprocess
from datetime import datetime, timezone

MANIFEST_PATH = "/workspace/reproducibility_manifest.json"

# Load existing manifest (or create minimal scaffold)
if os.path.exists(MANIFEST_PATH):
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
else:
    manifest = {"sessions": {}}

# Append Stage 1 SECT execution record
with open("/workspace/architecture_profile/stage_1_environment_fingerprint.json") as f:
    env_fp = json.load(f)
with open("/workspace/architecture_profile/stage_1_patch_state.json") as f:
    patch_state = json.load(f)
with open("/workspace/architecture_profile/stage_1_cache_state.json") as f:
    cache_state = json.load(f)
with open("/workspace/stage_1_sect/aggregate_verdict.json") as f:
    aggregate = json.load(f)
with open("/workspace/stage_1_sect/nv_inventory.json") as f:
    nv_inventory = json.load(f)

session_record = {
    "session": "2.6 — Stage 1 SECT execution",
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "target_model": "meta-llama/Llama-3.1-8B",
    "stage_1_verdict": aggregate["stage_1_verdict"],
    "trials_executed": aggregate["trials_executed"],
    "session_halted": aggregate["session_halted"],
    "halt_reason": aggregate.get("halt_reason"),
    "environment_fingerprint": env_fp,
    "patch_state": patch_state,
    "cache_state": cache_state,
    "aggregate_verdict_summary": {
        "per_criterion_counts": aggregate["per_criterion_counts"],
        "aggregate_pass": aggregate["aggregate_pass"],
    },
    "nv_inventory_summary": {
        "json_artifact_count": len(nv_inventory["json_artifacts"]),
        "overlay_artifact_count": len(nv_inventory["overlay_artifacts"]),
        "session_nv_footprint_mb": nv_inventory["session_nv_footprint_mb"],
    },
    "patches_applied": patch_state["patches_applied"],
    "patches_required_but_not_applied": patch_state["patches_required_but_not_applied"],
}

manifest.setdefault("sessions", {})["2.6"] = session_record

with open(MANIFEST_PATH, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Cell 12: reproducibility manifest updated at {MANIFEST_PATH}")

# SSD mirror sync trigger (operator-side). Document the rsync command;
# operator executes from MBP via SSH-pipe-from-pod or runs in pod with mounted SSD.
# This cell DOES NOT execute the rsync (no mounted SSD in pod by default);
# it documents the canonical command and emits a log file.
rsync_cmd = (
    "rsync -avz --partial --info=progress2 "
    "/workspace/stage_1_sect/ "
    "<operator>@<mbp>:<ssd_mount>/llm-as-database/stage_1_sect/"
)

mirror_sync_doc = {
    "documented_at": datetime.now(timezone.utc).isoformat(),
    "status": "DOCUMENTED — operator to execute from MBP",
    "rsync_command_template": rsync_cmd,
    "source_paths": [
        "/workspace/stage_1_sect/",
        "/workspace/architecture_profile/stage_1_*.json",
    ],
    "destination_root_template": "<ssd_mount>/llm-as-database/stage_1_sect/",
    "verification_after_sync": "compare per-file SHA-256 prefixes from nv_inventory.json against mirror",
}

with open("/workspace/stage_1_sect/mirror_sync.log", "w") as f:
    json.dump(mirror_sync_doc, f, indent=2)

print(f"Cell 12: mirror sync command documented at /workspace/stage_1_sect/mirror_sync.log")
print(f"\nOperator action: execute rsync from MBP to mirror NV → SSD; verify via SHA-256 prefix match.")
print(f"\n=== Session 2.6 (Stage 1 SECT execution) complete. Verdict: {aggregate['stage_1_verdict']}. ===")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `reproducibility_manifest.json` contains `sessions["2.6"]` | True |
| `mirror_sync.log` written | True |
| Final stdout reports verdict | matches `aggregate.stage_1_verdict` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Manifest write fails | Recoverable | Investigate filesystem permissions; retry |
| Operator does not execute rsync | Out of scope | Documented for operator-side action; not gating |

---

# Part IX — Halt conditions (cross-cell index per OQ-S23-8 taxonomy)

This part consolidates halt conditions across cells, classified by the OQ-S23-8 failure-mode taxonomy.

## 9.1 Failure mode taxonomy (inherited from OQ-S23-8)

| Failure mode | In-process retry safe? | Restart required? | Cells where applicable |
|---|---|---|---|
| `ModuleNotFoundError` (package absent) | Yes | No | Cell 0 |
| `ImportError` (Python source missing) | Yes | No | Cell 0 |
| Python source-only version mismatch | Yes (with sys.modules purge) | No | Cell 0, Cell 2 |
| **C extension version mismatch** | **No** | **Yes** | Cell 0 (mandatory restart) |
| Runtime `OutOfMemoryError` | No | Yes (torch allocator state corrupted) | Cell 5, Cell 9 |
| **NaN/Inf in mutated weights** | **No** | **Yes (model state corrupted)** | Cell 9 |
| Hung cell with no progress > 15 min | Conditional | Conditional | Cell 9 (MEMIT edit) |

## 9.2 Halt class summary by cell

| Cell | Halt classes | Recovery |
|---|---|---|
| Cell 0 | Pre-flight / dep manifest | Re-run; mandatory kernel restart |
| Cell 1 | Pre-flight / hardware invariant | Halt; verify pod procurement |
| Cell 2 | Pre-flight / patch state | Re-apply patches from canonical script; resume |
| **Cell 3** | **Hard halt — cache provenance** | **Schedule pre-S2.6 fork-work; defer Session 2.6** |
| Cell 4 | Pre-flight / hparams schema | Recover corrected hparams from S2.5a |
| Cell 5 | Pre-flight / model load / arch | Investigate procurement |
| Cell 6 | Pre-flight / single-token | Halt; defer to corpus revision |
| Cell 7 | Baseline anomaly | Investigate; possibly OQ-S25-10 escalation |
| Cell 8 | None (deterministic enumeration) | n/a |
| **Cell 9** | **Inter-trial gate / NaN-Inf / Copy-Unmount allclose / unmount-band** | **Immediate session halt; forensics** |
| Cell 9 | Trial-level cons / gen / spec failure | Continue; tolerated by ≥8/9 aggregate |
| Cell 10 | None (aggregation) | n/a |
| Cell 11 | NV write missing | Re-run only missing artifacts |
| Cell 12 | Manifest write | Recoverable; retry |

## 9.3 Forensic-snapshot discipline on session halt

If Cell 9 triggers an immediate session halt (inter-trial gate, NaN/Inf, Copy-Unmount allclose, or unmount-band fail):

1. Do NOT continue to subsequent trials.
2. Do NOT terminate the pod.
3. Capture: `/workspace/stage_1_sect/trial_loop_log.json` (with halt reason recorded), the offending trial's per-trial JSON if persisted, and the offending trial's overlay snapshot.
4. Run Cell 11 to verify NV inventory of partial state.
5. Run Cell 12 to update manifest with `session_halted=True` record.
6. Then stop pod (NV state preserved for forensics).
7. Surface halt class + offending trial index to operator via final stdout block; document halt context in `/workspace/stage_1_sect/session_halted_summary.md` for Session 2.7 retrospective input. (R2.5)
8. Open Session 2.7 retrospective on the halt class.

---

# Part X — Forward routing (Session 2.7 prep)

## 10.1 Session 2.7 — Stage 1 retrospective + Stage 2 sweep design

**Blocked on:** Stage 1 verdict in hand (this session's `aggregate_verdict.json`).

**Scope (PASS scenario):**

- Acceptance band fitness review (closes OQ-PROBE-2 if Stage 1 results inform calibration)
- Per-fact retrospective: was cfb-003 BPE-fragmentation impact (OQ-S25-7) detectable in trial verdicts?
- `mom2_update_weight=15000` validation (OQ-S25-3) — did MEMIT edit magnitudes look healthy across all 9 trials?
- `v_lr=0.5` SwiGLU dynamics retrospective (OQ-S25-4)
- Stage 2 sweep design: incorporates cfb-004, cfb-005 + variant-template substrate; addresses OQ-S25-5 (variant-template baseline-prior weakness)
- CFB v2 polysemy probe authorship scope (OQ-S25-6)

**Scope (FAIL scenario):**

- Failure-class diagnosis: which criterion failed, on which trials
- Hparams sweep candidates if generalization or specificity drift dominate failure
- BPE fragmentation deep-dive if cfb-003 dominates failure
- Possible runbook revision before re-execution

## 10.2 Workstream 3 implementation planning hooks

If Stage 1 PASS, the empirical evidence for `.vindex` overlay isolation as bit-identity (per Block 2 OQ-S23-11) is reinforced. Workstream 3 implementation planning may elevate the spec invariant per OQ-S23-11 with Stage 1 evidence cited.

## 10.3 Operator post-session checklist (post-runbook execution)

After Cell 12 completes (regardless of PASS / FAIL / halt outcome):

- [ ] Execute rsync from MBP per `/workspace/stage_1_sect/mirror_sync.log` template
- [ ] Verify per-file SHA-256 prefixes from `/workspace/stage_1_sect/nv_inventory.json` match SSD mirror copy
- [ ] Update `reproducibility_manifest.json` `sessions["2.6"]` with `mirror_sync_completed: true` (operator-edit on MBP) once verification succeeds
- [ ] Stop pod (NV preserves all session state automatically per D-S25-8)
- [ ] Post Session 2.6 closure note to project chat: verdict, halt reason if applicable, total wall time, total cost
- [ ] Schedule Session 2.7 (Stage 1 retrospective + Stage 2 sweep design) — input artifacts: aggregate verdict + per-trial JSONs + (if halted) `session_halted_summary.md`

---

# Part XI — Open questions in scope (closure paths)

## 11.1 OQs closed by this runbook's execution

| OQ ID | Closure mechanism in this runbook |
|---|---|
| **OQ-S25-1** | Cell 3 specifies canonical cache path schema (`<canonical>/wikipedia_stats/<file>`) and verifies file naming pattern (`model.layers.{L}.mlp.down_proj_float32_mom2_100000.npz`); closes via authoritative documentation |
| **OQ-CFB-2** (LLaMA-side) | Cell 6 single-token verification PASS for all 3 stage_1_eligible facts |
| **OQ-S25-9** | Cell 3 PROVENANCE.txt assertion; closure conditional on pre-S2.6 fork-work having produced fresh cache |
| **OQ-S25-10** | Cell 7 `stage_1_llama_baselines.json` produced; supersedes GPT-J baselines for trial verdicts |

## 11.2 OQs that this runbook activates / surfaces empirical data for

| OQ ID | Mechanism |
|---|---|
| **OQ-PROBE-2** (acceptance band calibration) | Cell 9 trial verdicts provide empirical drift distributions; Session 2.7 calibration input |
| **OQ-S25-3** (`mom2_update_weight=15000` for LLaMA) | Cell 9 MEMIT edit wall times + delta norms surfaced per trial; Session 2.7 retrospective |
| **OQ-S25-4** (`v_lr=0.5` SwiGLU dynamics) | same as OQ-S25-3 |
| **OQ-S25-7** (BPE fragmentation impact, cfb-003 keys on 'ky') | cfb-003 trial verdicts vs cfb-001/002 — Session 2.7 retrospective |

## 11.3 OQs explicitly out of scope for this runbook

| OQ ID | Reason |
|---|---|
| OQ-CFB-3 (template-sensitivity gradient — third template class) | Deferred to v2 / Stage 2 sweep design |
| OQ-S25-5 (variant-template baseline-prior weakness) | cfb-004/005 are Stage-2-only; not in Stage 1 trial set |
| OQ-S25-6 (polysemy probe authorship for CFB v2) | Post-Stage-2 |
| OQ-S23-10 (`past_key_values` Cache API migration) | MEMIT fork future task |
| OQ-S23-11 (`.vindex` bit-identity spec elevation) | Workstream 3 implementation planning |

---

# Part XII — Reference appendices

## 12.1 Acceptance bands (consolidated)

| Band | Threshold | Provenance | Provisional? |
|---|---|---|---|
| Consistency `p_target_new_post` | `> 0.5` | D-S24-10 | Yes (OQ-PROBE-2) |
| Generalization `drift_p_top_1` | `< 0.05` | D-S24-10 | Yes |
| Shared specificity `drift_p_top_1` (post-edit + post-unmount) | `< 0.05` | D-S24-10 | Yes |
| Unmount intra-pod drift `abs(p_target_true_postunmount − p_target_true_pre)` | **`< 1e-4`** | **IC-S23-4** | **No (HARD)** |
| Inter-trial baseline-drift gate (session invariant) | `< 1e-4` per shared-spec probe | runbook design (this session) | No (mirrors unmount band) |
| Aggregate per-criterion threshold (cons / gen / spec) | `≥ 8/9` | runbook design | Yes |
| Aggregate unmount threshold | **`9/9`** | C-S24-8 | **No (HARD)** |

## 12.2 Active probe count for Stage 1

| Class | Per-fact | Across 3 facts | Shared | Total active | Per-trial probe runs |
|---|---|---|---|---|---|
| Consistency | 3 | 9 | — | 9 | 3 (post-edit, for the active fact only) |
| Generalization | 3 (incl. 1 leakage on cfb-002) | 9 | — | 9 | 3 (post-edit) |
| Specificity (per-fact) | 0 (polysemy dropped per D-S25-1) | 0 | — | 0 | 0 |
| Specificity (shared) | — | — | 3 | 3 | 6 (3 post-edit + 3 post-unmount) |
| Unmount | 1 | 3 | — | 3 | 1 (post-unmount) |
| **Total** | — | — | — | **24** | **13 per trial** (cfb-001/002/003 alike) |

Pre-edit baseline (Cell 7) captures all 24 probes once. Per trial (Cell 9): 13 forward passes + 1 MEMIT edit + 1 Copy-Unmount.

## 12.3 Fact ID quick reference (Stage-1-eligible)

| Fact ID | Subject | target_new | target_true | LLaMA pre-edit P(target_true) |
|---|---|---|---|---|
| cfb-001 | Michael Jordan | baseball | basketball | ~0.55 (S2.5a smoke test; Cell 7 re-verifies) |
| cfb-002 | Tom Brady | soccer | football | TBD (Cell 7) |
| cfb-003 | Wayne Gretzky | tennis | hockey | TBD (Cell 7) |

## 12.4 Cell-to-constraint traceability

| Constraint | Cell of realization |
|---|---|
| C-S25-1 (filename autolinker) | Operator hygiene (Part II §2.4) |
| C-S25-2 (container-disk non-persistent) | Cell 0 (mandatory dep reinstall) |
| C-S25-3 (tool aliasing) | Operator hygiene (Part II §2.4) |
| C-S25-4 (HF token gated permission) | Operator preconditions (Part II §2.4) |
| C-S25-5 (MEMIT cwd invariant) | Cells 2, 4, 9 (`os.chdir`) |
| C-S25-6 (MEMIT dep manifest reinstall) | Cell 0 |
| C-S25-7 (pandas runtime deps) | Cell 0 phase 3 |
| C-S25-8 (hparams 20-field strict schema) | Cell 4 |
| C-S25-9 (P-4 config-attribute patch) | Cell 2 verification + applied to NV in S2.5a |
| C-S25-10 (bridge cache provenance restriction) | Cell 3 hard gate |
| C-S25-11 (fresh cache mandate) | Cell 3 hard gate |
| C-S25-12 (LLaMA baseline re-capture) | Cell 7 |
| C-S24-1 (Stage 1 eligibility partition) | Cell 8 trial matrix |
| C-S24-2 (MEMIT input format) | Cell 8 `fact_memit_requests` |
| C-S24-3 (single-token target invariant) | Cell 6 |
| C-S24-7 (leakage exclusivity) | Cell 8 (trivially satisfied; documented) |
| C-S24-8 (unmount band non-provisional) | Cell 9 unmount-band immediate halt |
| IC-S23-4 (intra-pod drift band 1e-4) | Cell 9 unmount band |
| IC-S24-3 (CFB v1 ↔ MEMIT input contract) | Cell 8 + Cell 9 |
| IC-S24-4 (Stage 1 trial protocol) | Cells 8 + 9 |
| IC-S25-1 (bridge cache provenance contract) | Cell 3 hard gate |
| IC-S25-2 (P-4 patch application contract) | Cell 2 verification |
| IC-S25-3 (LLaMA baseline re-capture contract) | Cell 7 |

## 12.5 NV-resident artifact paths (final state)

```
/workspace/architecture_profile/
  ├── meta-llama_Llama-3.1-8B.json                      (S2.5a; consumed by Cell 4)
  ├── stage_1_environment_fingerprint.json              (Cell 1 output)
  ├── stage_1_patch_state.json                          (Cell 2 output)
  ├── stage_1_cache_state.json                          (Cell 3 output)
  ├── stage_1_token_verification.json                   (Cell 6 output)
  └── stage_1_llama_baselines.json                      (Cell 7 output; IC-S25-3)

/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/
  ├── PROVENANCE.txt                                    (pre-S2.6 fork-work; consumed by Cell 3)
  └── (5 cache files, one per edit layer)               (pre-S2.6 fork-work)

/workspace/stage_1_sect/
  ├── trial_matrix.json                                 (Cell 8 output)
  ├── trials/
  │   ├── stage_1_trial_cfb-001_r1.json                 (Cell 9 per-trial output)
  │   ├── stage_1_trial_cfb-001_r2.json
  │   ├── stage_1_trial_cfb-001_r3.json
  │   ├── stage_1_trial_cfb-002_r1.json
  │   ├── stage_1_trial_cfb-002_r2.json
  │   ├── stage_1_trial_cfb-002_r3.json
  │   ├── stage_1_trial_cfb-003_r1.json
  │   ├── stage_1_trial_cfb-003_r2.json
  │   └── stage_1_trial_cfb-003_r3.json
  ├── overlays/
  │   ├── cfb-001/r1/{edited.pt, original.pt}
  │   ├── cfb-001/r2/{edited.pt, original.pt}
  │   ├── cfb-001/r3/{edited.pt, original.pt}
  │   ├── cfb-002/r1/{edited.pt, original.pt}
  │   ├── cfb-002/r2/{edited.pt, original.pt}
  │   ├── cfb-002/r3/{edited.pt, original.pt}
  │   ├── cfb-003/r1/{edited.pt, original.pt}
  │   ├── cfb-003/r2/{edited.pt, original.pt}
  │   └── cfb-003/r3/{edited.pt, original.pt}
  ├── trial_loop_log.json                               (Cell 9 consolidated)
  ├── aggregate_verdict.json                            (Cell 10 — Stage 1 verdict)
  ├── nv_inventory.json                                 (Cell 11 output)
  └── mirror_sync.log                                   (Cell 12 output)

/workspace/reproducibility_manifest.json                (Cell 12 update; sessions["2.6"])
```

## 12.6 Wall-time budget per cell (estimate)

| Cell | Wall time | Notes |
|---|---|---|
| Cell 0 | ~5–8 min | dep install + kernel restart |
| Cell 1 | ~30 sec | fingerprint capture |
| Cell 2 | ~30 sec | patch verification |
| Cell 3 | ~1 min | provenance check + cache file SHA-256 |
| Cell 4 | ~30 sec | hparams stage + load |
| Cell 5 | ~2–4 min | model load from NV-cached HF (~16 GB) |
| Cell 6 | ~30 sec | tokenizer single-token verification |
| Cell 7 | ~2–4 min | 24 forward passes + per-fact baseline |
| Cell 8 | ~10 sec | trial matrix definition |
| Cell 9 | ~50–70 min | 9 trials × ~5–7 min (MEMIT edit dominates) |
| Cell 10 | ~10 sec | aggregation |
| Cell 11 | ~30 sec | NV inventory + SHA-256 prefixes |
| Cell 12 | ~10 sec | manifest update |
| **Total** | **~70–95 min** | within OQ-S25-2 envelope |

---

*End of Stage 1 SECT Runbook for Session 2.6 execution.*
