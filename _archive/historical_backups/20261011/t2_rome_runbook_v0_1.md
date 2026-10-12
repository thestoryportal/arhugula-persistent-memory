# T.2 ROME Runbook v0.1 — meta-llama/Llama-3.1-8B

> **Authoring session:** S2.17 Block 2 (this session)
> **Predecessor session:** S2.16 (Framework Finding Archival + T-Branch Entry Scoping; CLOSED 2026-05-04)
> **Consumer session:** S2.18 — T.2 ROME execution
> **Target environment:** RunPod RTX 4090 24 GB single GPU; NV `large_amethyst_wolverine` (carry-forward)
> **Target model:** `meta-llama/Llama-3.1-8B` (base; not Instruct; SHA pin `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b`)
> **Write engine:** ROME (`https://github.com/kmeng01/rome`; SHA placeholder per D-S217-Q2-1; resolved at Block A Cell 1)
> **Trial protocol:** IC-S24-4 — 5 facts × 3 replicates = 15 trials; single-fact dispatch (C-ROME-1)
> **Cell pattern:** Three-block structure (Block A: setup + baseline; Block B: HC-2-equivalent dry-run; Block C: 15-trial loop) per `t2_rome_runbook_v0_1_authoring_plan.md` §2; structurally inherits from `stage_1_sect_runbook_v1_6.md` RATIFIED template
> **Specialists:** framework-spec-writer (primary, runbook authoring); memit-specialist (Cells 1, 2, 4, 8, 9, 11, 15 — ROME mechanism); state-consistency-theorist (Cells 3, 15 — covariance cache reuse + Copy-Unmount); validation-contract-architect (Cells 6, 7, 10, 12, 13, 16 — verdict surface)
>
> **Document version:** v0.1 (first synthesis at S2.17 Block 2)
> **Status:** RATIFIED v0.1 for S2.18 execution. Inherits the v1.6 hardening fixes from `stage_1_sect_runbook_v1_6.md` per D-S216-CLOSE-4 (v1.6 inheritance branch active per D-S216-Q5-1 = INLINE).
>
> **Inheritance manifest.** This runbook structurally inherits from `stage_1_sect_runbook_v1_6.md` RATIFIED at S2.17 Block 1 close. Specifically:
> - **Cell 0** (pod attach + NV mount) — inherited unchanged
> - **Cell 1** (environment fingerprint) — adapted: ROME-specific ENV fingerprint adds `rome_sha`, `rome_clone_url`
> - **Cell 1.5** (environment fingerprint manifest write) — inherited; `EXPECTED_KEYS` schema extended for ROME fingerprint
> - **Cell 2** (patch state verification) — adapted: 6-marker subset per `rome-patches-canonical.md` v0.1 §1 + §5 (P-1/P-2/P-4×2/P-5/P-6-verification-only); P-7 explicitly skipped
> - **Cell 3** (cache provenance gate) — inherited: SUBSET assertion pattern per D-S215D2-CELL3-SUBSET-ASSERTION-1 + v1.6 hardening
> - **Cell 4** (hparams) — adapted: ROME hparam schema (paper Table 1 GPT-J reference values per D-S217-Q3-1)
> - **Cell 5** (model load + Pad-Token) — inherited unchanged
> - **Cell 6** (tokenizer single-token verification) — inherited: cfb-v3 facts; D-S217-2 single-source contract
> - **Cell 7** (pre-edit baseline + target_TRUE capture) — inherited: D-S213C-CALIB-1/2/3 calibration-band stratification; 38 active probes
> - **Cell 8** (R1.3-equivalent dry-run gate) — adapted: ROME's `apply_rome_to_model` → `get_cov` resolution path
> - **Cells 9-13** (Block B HC-2-equivalent dry-run) — NEW: not in MEMIT runbook
> - **Cell 14** (trial matrix authoring) — inherited: 5×3=15 trials; D-S217-2 cross-cell SUBSET gate
> - **Cell 15** (trial loop execution) — adapted: single-fact ROME dispatch (no batched 5-fact); Copy-Unmount per-fact-narrowed
> - **Cells 16-20** (verdict aggregation + persistence) — inherited from MEMIT Cells 10-12 with cell-numbering shift

---

## 1.5 Authoring discipline — inheritance from v1.6 (C-S26-3 / D-S28-2 carry-forward)

This runbook v0.1 is authored at S2.17 Block 2 under inheritance from `stage_1_sect_runbook_v1_6.md` § §1.5 (RATIFIED at S2.17 Block 1). The C-S26-3 dry-run gate constraint and the D-S28-2 R1.3 codification carry forward to T.2 ROME via C-ROME-3 (`rome-patches-canonical.md` v0.1 §4.3).

> **C-ROME-3 (parallel to C-S26-3):** Runbook hardening passes targeting the ROME cache-dispatch surface require an R1.3-equivalent dry-run gate at Block A Cell 8 against post-patch NV state — REQUIRED before authoring-acceptance ratification of any v0.x → v0.(x+1) advance.

**v0.1 dry-run status: AUTHORING-ACCEPTANCE-DECLARATIVE.** This v0.1 is authored offline (no pod execution at S2.17). The full ratification gate (Block A Cell 8 R1.3-equivalent dry-run against post-clone NV state) is executed at S2.18 Block A first execution. v0.1 ships under DECLARATIVE status; v0.2 absorbs the empirical first-execution verdict.

| Gate | Trigger | v0.1 disposition at S2.17 Block 2 close |
|---|---|---|
| Authoring acceptance | All §6 acceptance criteria of `t2_rome_runbook_v0_1_authoring_plan.md` met; cell skeleton complete; v1.6 inheritance manifest declared | **RATIFIED v0.1** at S2.17 Block 2 close (declarative; no pod-side execution in this session) |
| C-ROME-4 application | New defense-in-depth marker added to v0.1 | NOT TRIGGERED — v0.1 contains zero new markers; all marker references inherited from MEMIT canonical via shared-codebase application |
| Cache-dispatch semantics preservation | v0.1 change to Cells 3, 5, 15 cache-dispatch surfaces relative to MEMIT Cells 3, 5, 9 | TRIGGERED — Cell 15 introduces single-fact ROME dispatch, which differs from MEMIT Cell 9's batched multi-fact projection. R1.3-equivalent gate at Block A Cell 8 is the dispatch-path verification anchor at S2.18 first execution |
| Empirical anchor inheritance | covariance caches L2-L8 + cross-session bit-exact determinism + Copy-Unmount L4-L8/L2-L6 | TRIGGERED — v0.1 inherits all three carry-forward anchors per D-S216-CLOSE-2 |

**Cross-reference.** `rome-patches-canonical.md` v0.1 §4 (process constraints); `stage_1_sect_runbook_v1_6.md` § §1.5 / §1.5.1 / §1.5.2 (parent constraints).

### 1.5.1 Single-fact dispatch envelope (D-S217-3; closes deferred OQ class)

> **D-S217-3.** ROME edit invocations at S2.18 Block C are single-fact, single-layer. The 15-trial Stage 1 SECT v3 protocol is executed as **15 sequential single-fact ROME edits**, not as a batched multi-fact ROME edit. Each trial's Copy-Unmount restore is per-fact, not per-trial-group.

**Empirical motivation.** ROME's published mechanism is single-fact rank-1 update; batched ROME invocation is not a documented mode of the canonical implementation (`https://github.com/kmeng01/rome`). The MEMIT-vs-ROME comparison framework finding (deferred to S2.19+ per D-S216-CLOSE-5) is testable only when ROME's intrinsic single-fact mechanism is preserved at execution.

### 1.5.2 Empirical anchor inheritance (D-S217-4)

> **D-S217-4.** v0.1 inherits the following empirical anchors without re-execution at S2.17:
> 1. **Cross-session bit-exact determinism** on Llama-3.1-8B fp16: 5 cross-session checkpoints; forward-pass drift `0.00e+00`. Source: S2.14-D `OQ-S214D-DETERMINISM-1` closed empirically.
> 2. **Copy-Unmount bit-exact joint-overlay regime:** L4-L8 (S2.14-D D.3) + L2-L6 (S2.15-D2 D.2); 75/75 + 5/5 layer-restore allclose; per-fact unmount drift `0.00e+00`. Source: S2.14-D `OQ-S214D-D3-3` + S2.15-D2 narrowed-window. Carry-forward to ROME single-fact regime is structurally narrower (1 layer per fact, not 5); the validated regime is a strict superset.
> 3. **Covariance caches L2-L8** durable on NV `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/`; 5.75 GB; PROVENANCE-narrowed cumulative. Source: pre-S2.6 fork-work session + S2.13-C / S2.14-D / S2.15-D2 reuse.
> 4. **`stage_1_llama_baselines.json`** 38-probe baseline at canonical hparams; cfb-v3 fact roster; pre-edit `P[target_TRUE]` natural top-1 captured per D-S213C-CALIB-1/2/3.

**Re-execution at S2.18 Cell 5 / Cell 7:** Cells 5 + 7 re-execute the baseline capture against the loaded model state to verify the cross-session anchor under the pod's current state. Drift > 0 at any of the 38 probes triggers session-level halt + investigation; this is the bit-exact gate that anchors all post-edit verdicts.

---

# Part I — Session orientation

## 1.1 Purpose

This runbook drives Session 2.18 — the first T.2 ROME execution against the Workstream 1 production target model `meta-llama/Llama-3.1-8B`. It executes:

1. **Block A** — pre-flight verification (pod, NV, ROME repo clone, patches, covariance cache reuse, hparams, model load, tokenizer, baseline capture, R1.3-equivalent dry-run gate) at Cells 0-8
2. **Block B** — HC-2-equivalent dry-run (single edit on cfb-v3-001 guitar at Layer-A=L17 primary, then at Layer-B=L2 secondary; cross-layer comparison; load-bearing layer selection) at Cells 9-13
3. **Block C** — 15-trial Stage 1 SECT v3 execution at single-fact ROME dispatch on the load-bearing layer; per-trial verdict aggregation; aggregate verdict per D-S215D2-VERDICT-INTEGRITY-1 carry-forward at Cells 14-20

T.2 ROME is the load-bearing empirical step that tests whether the architectural-invariant ceiling on (Llama-3.1-8B × MEMIT × canonical hparams) — confirmed at six orthogonal axes per `framework_finding_memit_ceiling_archival.md` v1.0 — is **structural to MEMIT specifically**, OR **structural to (Llama-3.1-8B × any rank-1 in-weight write engine)**. T.2 ROME PASS routes the framework finding to a MEMIT-specific ceiling characterization (S2.19 = MEMIT-vs-ROME comparison); T.2 ROME FAIL escalates to GRACE adapter-based testing per D-S216-Q3-1.

## 1.2 Measures

Per IC-S24-4 trial protocol carry-forward (single-fact narrowing per C-ROME-1), each of the 15 trials produces a verdict against four criteria. Acceptance bands inherit from MEMIT canonical (D-S24-10 + IC-S23-4); under ROME single-fact dispatch the unmount band is narrower (1 edited layer to restore vs MEMIT's 5).

| Criterion | Definition | Acceptance band | Provenance |
|---|---|---|---|
| **Consistency** | Post-edit top-1 token equals `target_new` and `P(target_new)` exceeds 0.5 | `p_target_new_post > 0.5` | Provisional (D-S24-10; OQ-PROBE-2 carry-forward) |
| **Generalization** | Pre-edit→post-edit drift in top-1 probability for related-but-unedited probes is small | `abs(p_top_1_post − p_top_1_pre) < 0.05` per probe | Provisional |
| **Specificity (shared)** | Pre-edit→post-edit drift in top-1 probability for shared-specificity probes (cross-fact unrelated subjects) is small | `abs(p_top_1_post − p_top_1_pre) < 0.05` per probe | Provisional |
| **Unmount intra-pod drift** | post-Copy-Unmount drift on `target_TRUE` for the edited fact | `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4` | **HARD** (IC-S23-4) |

**Calibration-band stratification carry-forward (D-S213C-CALIB-3):** the PASS-set is the 4-of-17 instrument single-token coverage subset on the Llama tokenizer. cfb-v3-003 violin / cfb-v3-005 flute carry calibration-band stratification annotations; cfb-v3-004 harp under multi-token allowlist with **first-token-proxy per D-S217-Q5-1** (carry-forward of D-S215D2-CFB-V3-004-PROXY-1 + D-S215D2-CFB-V3-004-MULTITOKEN-1) AND `RE-EVALUATE AT TRIAL 0` flag at Block B Cell 13.

## 1.3 Verdict integrity binding (D-S215D2-VERDICT-INTEGRITY-1 carry-forward)

> **Carry-forward from S2.15-D2.** Aggregate verdict at Cell 17 is computed against the **load-bearing subset** {cfb-v3-001, cfb-v3-002, cfb-v3-005} as decisive; full 5-fact aggregate is informational only. cfb-v3-003 and cfb-v3-004 are forensic-informative-excluded by default per S2.13-C calibration-band stratification, MODULO Block B Cell 13 OQ-S217-1 resolution (Q5; cfb-v3-004 multi-token tolerance posture under ROME's single-fact dispatch — first-token-proxy carry-forward at v0.1 with explicit re-evaluation at trial 0).

## 1.4 Halt conditions (cross-cell index)

| Condition | Class | Action |
|---|---|---|
| Pod attach failure (Cell 0) | Pre-flight | Re-attach; if persistent, escalate operator |
| ROME repo clone failure (Cell 1) | Pre-flight | Verify network; verify SHA pin resolution; halt session if persistent |
| Patch verification failure (Cell 2) | Pre-flight | Per `rome-patches-canonical.md` v0.1 §1 — schedule fork-work-equivalent ROME patch application session; halt this session |
| Covariance cache failure (Cell 3) | Session-level | Hard halt; cache reuse precondition broken; investigate NV state; do not re-compute cache without operator authorization |
| ROME hparam schema validation failure (Cell 4) | Pre-flight | Re-author Cell 4 hparam dict; re-load |
| Model load OOM (Cell 5) | Pre-flight | Restart kernel; re-verify VRAM baseline; per MEMIT runbook v1.6 Cell 0 §0.6 hygiene |
| Tokenizer single-token failure (Cell 6) | Session-level | Halt; revise affected fact; re-version cfb-v3 corpus; defer Stage 1 to v1.1 corpus |
| Baseline drift > 0 against carry-forward `stage_1_llama_baselines.json` (Cell 5 / Cell 7) | Session-level | Hard halt — cross-session bit-exact determinism violated; investigate model SHA, HF cache state, P-1/P-2 application, BEFORE proceeding |
| R1.3-equivalent gate FAIL (Cell 8) | Session-level | Hard halt — cache-dispatch round-trip broken under ROME path; verify `rome/layer_stats.py` post-P-6 form; investigate ROME's `get_cov` invocation |
| Block B verdict failure (Cell 13) | Session-level (Block B) | If both layer candidates FAIL the calibration corridor: ROME single-fact dispatch on Llama-3.1-8B does not produce in-band edits at any tested layer → escalate to D-S216-Q3-1 escalation path (GRACE) |
| Unmount band drift > 1e-4 at any trial (Cell 15) | Trial-level (HARD per IC-S23-4) | Immediate halt at the violating trial; do not proceed to next trial; preserve overlay snapshot for forensics |
| Inter-trial baseline drift > 1e-4 on shared-spec probes (Cell 15) | Trial-level (HARD) | Immediate halt; investigate Copy-Unmount restore integrity |

---

# Part II — Pod configuration

## 2.1 Carry-forward from MEMIT runbook v1.6

Pod configuration (RunPod RTX 4090 24 GiB; NV `large_amethyst_wolverine`; Python 3.11; HF env-vars per `stage_1_sect_runbook_v1_6.md` Cell 0 §0.4 PRE-INJECT; etc.) is INHERITED unchanged. T.2 ROME does not introduce pod-level configuration changes.

## 2.2 NV state expected at S2.18 entry

| Path | Source | Cell that consumes |
|---|---|---|
| `/workspace/memit_dry_run/memit/` | pre-S2.6 fork-work + S2.7 patch application | (preserved; not consumed by T.2 ROME) |
| `/workspace/rome_dry_run/rome/` | **NEW at S2.18 Block A Cell 1** — clone of `https://github.com/kmeng01/rome` at resolved SHA | Cell 2 (patch verification) |
| `/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json` | S2.5a baseline | Cell 4 (hparam staging) |
| `/workspace/architecture_profile/stage_1_llama_baselines.json` | S2.13-C / S2.15-D2 cumulative | Cell 5 (cross-session bit-exact gate) + Cell 7 (re-capture comparison) |
| `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` | pre-S2.6 fork-work | Cell 3 (SUBSET reuse verification) |
| `/workspace/covariance_caches/.../wikipedia_stats/PROVENANCE.txt` | pre-S2.6 fork-work | Cell 3 (provenance gate) |
| `/workspace/reproducibility_manifest.json` | cumulative | Cell 19 update at S2.18 close |

---

# Part III — Block A: setup, patches, baseline capture (Cells 0–8)

## Cell 0 — System binaries + Python deps

**Specialist:** framework-spec-writer (carry-forward orchestration)

**Purpose:** Pod attach verification + dependency installation + Jupyter kernel hygiene + HF env-var injection. **INHERITED UNCHANGED from `stage_1_sect_runbook_v1_6.md` Cell 0** — see that runbook §0.1 through §0.7 for full cell content. The only difference: at S2.18 entry, the operator may want to verify the additional dependency `git` is present (used at Cell 1 for ROME repo clone — typically present on RunPod images).

**Verification anchors:** Same as MEMIT runbook v1.6 Cell 0 — see anchors there.

**Halt conditions:** Same as MEMIT runbook v1.6 Cell 0 — see halts there.

---

## Cell 1 — ROME repository clone + SHA pin resolution

**Specialist:** memit-specialist (ROME mechanism orientation)

**Purpose:** Clone `https://github.com/kmeng01/rome` to `/workspace/rome_dry_run/rome/` at resolved SHA. Per D-S217-Q2-1, the SHA is "latest stable tip" — captured at first execution. Subsequent executions verify the SHA pin is preserved.

**Inputs:** Network access to GitHub; NV write permission at `/workspace/rome_dry_run/`.

```python
# === CELL 1 — ROME repository clone + SHA pin resolution ===
# Specialist: memit-specialist
# References: D-S217-Q2-1 (SHA pin = latest stable tip);
#             rome-patches-canonical.md v0.1 §2 (SHA pin semantics)

import os, subprocess
from datetime import datetime, timezone

ROME_CLONE_URL = "https://github.com/kmeng01/rome"
ROME_ROOT = "/workspace/rome_dry_run/rome"

# v0.1 SHA pin resolution: at first execution, pin = latest stable tip;
# resolved SHA captured to environment_fingerprint manifest at Cell 1.5.
# Subsequent executions: SHA pin = the previously-resolved SHA, asserted equal.
PINNED_ROME_SHA_PATH = "/workspace/architecture_profile/t2_rome_pinned_sha.txt"

if not os.path.exists(ROME_ROOT):
    # First execution: clone latest stable
    os.makedirs(os.path.dirname(ROME_ROOT), exist_ok=True)
    subprocess.run(
        ["git", "clone", ROME_CLONE_URL, ROME_ROOT],
        check=True
    )
    # Capture resolved SHA
    rome_sha = subprocess.check_output(
        ["git", "-C", ROME_ROOT, "rev-parse", "HEAD"], text=True
    ).strip()
    # Persist pinned SHA for subsequent executions
    os.makedirs(os.path.dirname(PINNED_ROME_SHA_PATH), exist_ok=True)
    with open(PINNED_ROME_SHA_PATH, "w") as f:
        f.write(rome_sha + "\n")
    print(f"Cell 1 (first execution): cloned ROME at SHA {rome_sha}")
    print(f"  Pinned SHA captured to {PINNED_ROME_SHA_PATH}")
else:
    # Subsequent execution: verify SHA pin
    rome_sha = subprocess.check_output(
        ["git", "-C", ROME_ROOT, "rev-parse", "HEAD"], text=True
    ).strip()
    assert os.path.exists(PINNED_ROME_SHA_PATH), \
        f"Pinned SHA file missing at {PINNED_ROME_SHA_PATH}; first-execution capture lost. " \
        f"Halt and investigate NV state."
    with open(PINNED_ROME_SHA_PATH) as f:
        expected_rome_sha = f.read().strip()
    assert rome_sha == expected_rome_sha, \
        f"ROME SHA pin drift: got {rome_sha}, expected {expected_rome_sha}. " \
        f"HALT — repo state has drifted since first execution."
    print(f"Cell 1: ROME SHA pin verified at {rome_sha}")

# Verify directory structure: confirm key files exist
EXPECTED_ROME_FILES = [
    "rome/rome_main.py",
    "rome/compute_v.py",
    "rome/layer_stats.py",
    "util/nethook.py",
    "experiments/causal_trace.py",  # informational; used at S2.14-D forensic mediation
]
missing = [f for f in EXPECTED_ROME_FILES if not os.path.exists(os.path.join(ROME_ROOT, f))]
assert not missing, f"ROME repo structure unexpected: missing files {missing}. " \
                    f"HALT — verify clone integrity."

print(f"Cell 1: ROME directory structure verified at {ROME_ROOT}")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `ROME_ROOT` exists | True |
| `rome_sha` (40-char hex) | resolved at first execution; preserved at subsequent |
| `rome/rome_main.py` | present |
| `rome/compute_v.py` | present |
| `rome/layer_stats.py` | present (shared with MEMIT codebase) |
| `util/nethook.py` | present (shared with MEMIT codebase) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Network failure during clone | Pre-flight | Retry; verify network; verify GitHub reachability |
| SHA drift on subsequent execution | Pre-flight | Halt; investigate — repo state should not change between sessions |
| Missing expected file | Pre-flight | Halt; verify clone integrity; re-clone if needed |

---

## Cell 1.5 — Environment fingerprint capture

**Specialist:** framework-spec-writer (manifest discipline)

**Purpose:** Write `t2_rome_environment_fingerprint.json` with all version anchors. Schema parallels MEMIT runbook v1.6 Cell 1 with ROME-specific extensions.

```python
# === CELL 1.5 — Environment fingerprint capture (ROME-extended) ===
# Specialist: framework-spec-writer
# References: D-S217-4 empirical anchor inheritance; manifest discipline

import sys, json, subprocess, torch, transformers
from datetime import datetime, timezone

EXPECTED_KEYS = {
    "captured_at",
    "session_label",
    "python_version",
    "torch_version",
    "transformers_version",
    "rome_sha",                  # NEW for T.2 ROME
    "rome_clone_url",            # NEW for T.2 ROME
    "memit_sha",                 # carry-forward (preserved on NV; informational)
    "model_name",
    "model_revision_sha",        # populated at Cell 5 per OQ-S28-4 stage discipline
    "cuda_visible_devices",
    "gpu_name",
    "vram_gb",
    "hf_home",
}

env_fingerprint = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": "S2.18",   # operator confirms at first execution
    "python_version": sys.version,
    "torch_version": torch.__version__,
    "transformers_version": transformers.__version__,
    "rome_sha": rome_sha,        # from Cell 1
    "rome_clone_url": ROME_CLONE_URL,
    "memit_sha": "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b",  # carry-forward; NV-resident
    "model_name": "meta-llama/Llama-3.1-8B",
    "model_revision_sha": None,  # populated at Cell 5 post-load HfApi call
    "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "(unset)"),
    "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 2)
                  if torch.cuda.is_available() else None,
    "hf_home": os.environ.get("HF_HOME", "(unset)"),
}

# Schema gate
assert set(env_fingerprint.keys()) == EXPECTED_KEYS, \
    f"Schema drift: {set(env_fingerprint.keys()) ^ EXPECTED_KEYS}"

os.makedirs("/workspace/architecture_profile", exist_ok=True)
with open("/workspace/architecture_profile/t2_rome_environment_fingerprint.json", "w") as f:
    json.dump(env_fingerprint, f, indent=2)

print(f"Cell 1.5: environment fingerprint staged. ROME SHA: {rome_sha}")
print(f"  Llama model revision SHA: deferred to Cell 5 post-load.")
```

**Verification anchors:** all EXPECTED_KEYS present; SHA-pin discipline preserved.

**Halt conditions:** Schema drift = halt; re-author EXPECTED_KEYS dict.

---

## Cell 2 — ROME patch state verification

**Specialist:** memit-specialist (patch surface inventory; ROME-MEMIT shared-codebase verification)

**Purpose:** Verify that `/workspace/rome_dry_run/rome/` carries the patches required for ROME edit dispatch. Per `rome-patches-canonical.md` v0.1 §1 + §5: P-1, P-2, P-4 (dual site), P-5, P-6 (verification-only), Pad-Token (deferred to Cell 5), Copy-Unmount (deferred to Cell 15). P-3', Device-Map, P-7 are inapplicable.

**Inputs:** NV-resident `/workspace/rome_dry_run/rome/`; `rome_sha` from Cell 1.

```python
# === CELL 2 — ROME patch state verification ===
# Specialist: memit-specialist
# References: rome-patches-canonical.md v0.1 §1 (patch inventory) + §5 (application order) + §6 (manifest schema);
#             D-S217-1 carry-forward (Cell 2 = canonical marker site for ROME runbook also)

import os, hashlib, json
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════
# Patch P-1 + P-2 verification (util/nethook.py — shared with MEMIT)
# ═══════════════════════════════════════════════════════════════
nethook_path = f"{ROME_ROOT}/util/nethook.py"
with open(nethook_path) as f:
    nethook_src = f.read()

p1_marker = "def retain_hook(m, args, kwargs, output):"
p2_marker = "with_kwargs=True"
assert p1_marker in nethook_src, "P-1 (hook signature) not applied to ROME util/nethook.py"
assert p2_marker in nethook_src, "P-2 (with_kwargs registration) not applied to ROME util/nethook.py"

# ═══════════════════════════════════════════════════════════════
# Patch P-4 verification (rome/compute_v.py — hidden_size; rome/layer_stats.py — max_position_embeddings count ≥ 2)
# Per rome-patches-canonical.md v0.1 §1.1: P-4 site on memit/compute_z.py is INAPPLICABLE to ROME (no analogous file)
# ═══════════════════════════════════════════════════════════════
p4_compute_v_path = f"{ROME_ROOT}/rome/compute_v.py"
p4_layer_stats_path = f"{ROME_ROOT}/rome/layer_stats.py"

with open(p4_compute_v_path) as f:
    compute_v_src = f.read()
assert "hidden_size" in compute_v_src, \
    f"P-4 (hidden_size fallback) not applied in {p4_compute_v_path}"

with open(p4_layer_stats_path) as f:
    layer_stats_src = f.read()
def _count_substring(src, needle):
    return src.count(needle)
assert _count_substring(layer_stats_src, "max_position_embeddings") >= 2, \
    f"P-4 (max_position_embeddings dual-site fallback) not applied in {p4_layer_stats_path}; " \
    f"expected count ≥ 2, got {_count_substring(layer_stats_src, 'max_position_embeddings')}."

# ═══════════════════════════════════════════════════════════════
# Patch P-5 verification (rome/layer_stats.py — dataset loader modernization)
# ═══════════════════════════════════════════════════════════════
p5_post_markers = [
    '"20231101.en"',
    '"wikimedia/wikipedia"',
]
for marker in p5_post_markers:
    assert marker in layer_stats_src, \
        f"P-5 marker {marker!r} missing from {p4_layer_stats_path}"

# ═══════════════════════════════════════════════════════════════
# Patch P-6 verification-only (rome/layer_stats.py — f-string post-form)
# Per rome-patches-canonical.md v0.1 §1.5: this is a VERIFICATION GATE, not an application step
# ═══════════════════════════════════════════════════════════════
p6_post_marker = 'size_suffix = f"_t{batch_tokens}" + size_suffix'
assert p6_post_marker in layer_stats_src, \
    f"P-6 marker {p6_post_marker!r} missing from {p4_layer_stats_path}; " \
    f"shared rome/layer_stats.py file does not carry post-P-6 form. " \
    f"INVESTIGATE — pre-S2.6 fork-work session expectation violated."

# ═══════════════════════════════════════════════════════════════
# Verify P-7 site is NOT present in ROME (informational)
# Per rome-patches-canonical.md v0.1 §1.3: P-7 inapplicability anchor — memit_main.py does not exist in ROME
# ═══════════════════════════════════════════════════════════════
memit_main_in_rome = os.path.exists(f"{ROME_ROOT}/memit/memit_main.py")
assert not memit_main_in_rome, \
    f"Unexpected: memit/memit_main.py present in ROME repo. " \
    f"Repo structure does not match expectation (rome-patches-canonical.md v0.1 §1.3)."

# ═══════════════════════════════════════════════════════════════
# Patch state aggregation
# ═══════════════════════════════════════════════════════════════
import sys
if ROME_ROOT not in sys.path:
    sys.path.insert(0, ROME_ROOT)

patched_files = [nethook_path, p4_compute_v_path, p4_layer_stats_path, f"{ROME_ROOT}/rome/rome_main.py"]
file_hashes = {}
for path in patched_files:
    with open(path, "rb") as f:
        file_hashes[os.path.relpath(path, ROME_ROOT)] = hashlib.sha256(f.read()).hexdigest()[:16]

patch_state = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "rome_sha": rome_sha,
    "patches_verified": {
        "rome_nethook_p1_signature_and_inputs_synthesis": True,
        "rome_nethook_p2_with_kwargs_registration": True,
        "rome_compute_v_p4_hidden_size": True,
        "rome_layer_stats_p4_max_position_embeddings": True,
        "rome_layer_stats_p5_dataset_modernization": True,
        "rome_layer_stats_p6_fstring_post_form": True,
        "tokenizer_pad_token_alias": False,                # applied at Cell 5
        "copy_unmount_in_place_restore": False,            # applied at Cell 15
    },
    "patches_inapplicable": [
        "rome_p3_prime_cpu_offload",
        "rome_explicit_device_map",
        "rome_main_p7_get_cov_batch_tokens",
    ],
    "patches_applied_at_runtime": {
        "tokenizer_pad_token_alias": "Cell 5 (model load)",
        "copy_unmount_in_place_restore": "Cell 15 (trial fn body)",
    },
    "file_sha256_prefix": file_hashes,
}

with open("/workspace/architecture_profile/t2_rome_patch_state.json", "w") as f:
    json.dump(patch_state, f, indent=2)

# C-S25-5 carry-forward — adapted as ROME_ROOT cwd invariant
os.chdir(ROME_ROOT)

print(f"Cell 2: ROME patch state verified. P-1, P-2, P-4 (dual), P-5, P-6 (verification-only) all applied to NV-resident repo.")
print(f"  Inapplicable: P-3', Device-Map, P-7 (per rome-patches-canonical.md v0.1 §1.3)")
print(f"  Cwd: {os.getcwd()}")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| P-1 marker in `util/nethook.py` | present |
| P-2 marker in `util/nethook.py` | present |
| `hidden_size` in `rome/compute_v.py` | present |
| `max_position_embeddings` count in `rome/layer_stats.py` | ≥ 2 |
| P-5 markers in `rome/layer_stats.py` | both present |
| P-6 post-form in `rome/layer_stats.py` | present (verification-only) |
| `memit/memit_main.py` in ROME repo | NOT present (P-7 inapplicability anchor) |
| `os.getcwd()` | `/workspace/rome_dry_run/rome` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any P-1 / P-2 / P-4 / P-5 / P-6 marker absent | Pre-flight | Re-apply patch via fork-work-equivalent ROME application session; halt this session |
| `memit/memit_main.py` present in ROME repo | Pre-flight | Investigate — clone may have pulled an unexpected branch; verify `rome-patches-canonical.md` v0.1 §1.3 expectations |
| `os.getcwd()` not ROME_ROOT | Pre-flight | C-S25-5-equivalent violation; halt |

---

## Cell 3 — Covariance cache reuse verification

**Specialist:** state-consistency-theorist (cache reuse + PROVENANCE gate)

**Purpose:** Verify that the NV-resident covariance cache produced at the pre-S2.6 fork-work session (and validated cumulatively across S2.13-C / S2.14-D / S2.15-D2) is consumable by ROME's `apply_rome_to_model` → `get_cov` resolution chain. **Inherits the v1.6 SUBSET assertion pattern unchanged from `stage_1_sect_runbook_v1_6.md` Cell 3** (per D-S215D2-CELL3-SUBSET-ASSERTION-1 carry-forward; v1.6 hardening canonical form).

**Inputs:** NV-resident `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` (5+ `.npz` files + `PROVENANCE.txt`).

**Cell 3 implementation:** Direct carry-forward from `stage_1_sect_runbook_v1_6.md` Cell 3, with the following targeted differences:

1. **R1.1 SUBSET assertion** — inherited unchanged (closes OQ-S215D2-PROVENANCE-CACHE-TRUTH-1 transitively for ROME). PROVENANCE-declared layer_set MUST be a subset of cache truth; cache-truth-superset is acceptable.
2. **R1.2 internals consumer** — inherited unchanged (`mom2.mom2` priority resolution per IC-PreS26-3).
3. **R1.3 smoke-load** — adapted: at v0.1 the smoke-load uses ROME's `get_cov` invocation path with `_ConfigOnlyPlaceholder` rather than MEMIT's. The R1.3 binding under ROME tests whether `rome/layer_stats.py` (post-P-6) correctly resolves the cached `_t100_` filename when invoked through ROME's edit dispatch chain. **Empirical anchor at v0.1: declarative; first execution at S2.18 produces the empirical R1.3 verdict for ROME.**
4. **Cache state writer** — inherits the v1.6 canonical `provenance` field name (per OQ-S215D2-CELL11-CACHE-SHA-KEY-1 closure); writes to `t2_rome_cache_state.json`.

> **Per-layer cache requirement at ROME single-fact dispatch:** ROME edits one layer per fact; the layer is selected per OQ-S216-3 / D-S217-Q4-1 (L17 primary, L2 secondary at Block B). Cell 3's PROVENANCE-declared `layer_set` is the authoring-time **target sweep window** — at v0.1 the operator authors `layer_set = "[2, 17]"` (the two candidate layers) into PROVENANCE.txt before pod attach. The cache truth on NV is the cumulative L2-L8 set produced at predecessor sessions. SUBSET assertion: `{2, 17}` ⊆ cache truth — but cache truth is `{2,3,4,5,6,7,8}`, so **L17 is NOT in cache truth**. This is a **v0.1 dependency surface** that needs operator-side resolution before S2.18 entry: either (a) extend the cache to include L17 by running a layer_stats compute pass for L17 (estimated wall-time ~30 min on RTX 4090 against Wikipedia 100k samples), OR (b) restrict Block B Cell 11 layer candidate to L9-L17 range covered by available cache and re-author Q4 layer-set candidates.

**Operator decision deferred at v0.1: OQ-S217-2.** L17 covariance cache availability — extend cache OR restrict layer candidate. Resolution scope: **operator-side at S2.18 Block A entry, before pod attach.** Recommended: extend cache to include L17 (and L2 already covered) — preserves the L17 ROME paper precedent vs L2 mediation peak comparison surface at Block B.

**Halt conditions:** as MEMIT v1.6 Cell 3, with the SUBSET-violation halt class noting ROME-specific layer-set sweep window discipline.

---

## Cell 4 — ROME hparam declaration

**Specialist:** memit-specialist (hparam surface inventory; D-S217-Q3-1 ratification embedded)

**Purpose:** Construct ROME hparam dict for the layer candidates (L17 primary, L2 secondary) per `rome-patches-canonical.md` v0.1 §3.1. Stage to NV.

```python
# === CELL 4 — ROME hparam declaration ===
# Specialist: memit-specialist
# References: rome-patches-canonical.md v0.1 §3.1 (paper Table 1 GPT-J reference values);
#             D-S217-Q3-1 (canonical hparam starting values at v0.1)

import json

# v0.1 declared starting values per ROME paper Table 1 (GPT-J reference)
# Full Llama-3.1-8B calibration deferred to S2.18 Block B Cell 13
ROME_HPARAMS_LAYER_A = {  # L17 primary
    "layers": [17],
    "fact_token": "subject_last",
    "v_num_grad_steps": 20,
    "v_lr": 0.5,
    "v_loss_layer": 31,                   # placeholder; Llama 32-layer last-layer; calibrated at Block B
    "v_weight_decay": 0.5,
    "clamp_norm_factor": 4,
    "kl_factor": 0.0625,
    "mom2_adjustment": 15000,
    "mom2_n_samples": 100000,
    "mom2_dtype": "float32",
    "mom2_batch_tokens": 100,             # carry-forward C-S26-1; same Wikipedia cache
    "context_template_length_params": [[5, 10], [10, 10]],
    "rewrite_module_tmp": "model.layers.{}.mlp.down_proj",
    "layer_module_tmp": "model.layers.{}",
    "mlp_module_tmp": "model.layers.{}.mlp",
    "attn_module_tmp": "model.layers.{}.self_attn",
    "ln_f_module": "model.norm",          # Llama-specific; differs from GPT-J transformer.ln_f
    "lm_head_module": "lm_head",
    "stats_dir": "/workspace/covariance_caches",
    "mom2_dataset": "wikipedia",
}

ROME_HPARAMS_LAYER_B = dict(ROME_HPARAMS_LAYER_A)  # L2 secondary; same hparams modulo layer
ROME_HPARAMS_LAYER_B["layers"] = [2]

# 20-field schema gate (parallel to MEMIT C-S25-8)
EXPECTED_FIELDS = set(ROME_HPARAMS_LAYER_A.keys())
assert len(EXPECTED_FIELDS) == 20, f"Schema drift: {len(EXPECTED_FIELDS)} fields, expected 20"

hparam_manifest = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "version": "v0.1",
    "basis": "rome-patches-canonical.md v0.1 §3.1 (ROME paper Table 1 GPT-J reference; declared starting values)",
    "layer_a_primary": ROME_HPARAMS_LAYER_A,
    "layer_b_secondary": ROME_HPARAMS_LAYER_B,
    "calibration_status": "DECLARED — full calibration to Llama-3.1-8B at S2.18 Block B Cell 13",
}

with open("/workspace/architecture_profile/t2_rome_hparams.json", "w") as f:
    json.dump(hparam_manifest, f, indent=2)

print(f"Cell 4: ROME hparams declared (Layer-A=L17 primary; Layer-B=L2 secondary). "
      f"Schema gate: {len(EXPECTED_FIELDS)}/20 fields PASS.")
```

**Verification anchors:** 20 hparam fields × 2 layer candidates; declared starting values per ROME paper Table 1.

**Halt conditions:** Schema drift = halt; re-author EXPECTED_FIELDS dict.

---

## Cell 5 — Llama-3.1-8B model load + Pad-Token alias + cross-session bit-exact gate

**Specialist:** memit-specialist (model load) + state-consistency-theorist (Pad-Token + bit-exact gate)

**Purpose:** Load `meta-llama/Llama-3.1-8B` from NV-cached HF; apply Pad-Token alias; capture model_revision_sha to env_fingerprint; verify cross-session bit-exact determinism against `stage_1_llama_baselines.json` carry-forward. **INHERITED UNCHANGED from `stage_1_sect_runbook_v1_6.md` Cell 5.**

> **D-S217-4 cross-session bit-exact gate.** At first probe pass, the model's forward-pass output on each of the 38 active probes MUST match `stage_1_llama_baselines.json` (S2.13-C / S2.15-D2 cumulative) at fp16 forward-pass drift `0.00e+00`. Drift > 0 at any probe halts the session — cross-session bit-exact determinism is the load-bearing precondition for all post-edit verdicts.

**Cell 5 implementation:** Direct carry-forward from `stage_1_sect_runbook_v1_6.md` Cell 5; no ROME-specific changes.

---

## Cell 6 — LLaMA tokenizer single-token verification (cfb-v3 facts)

**Specialist:** validation-contract-architect (single-token invariant per C-S24-3)

**Purpose:** Verify cfb-v3 fact roster (5 facts; instrument-cluster targets) under Llama tokenizer. **INHERITED UNCHANGED from `stage_1_sect_runbook_v1_6.md` Cell 6, including the v1.6 D-S217-2 single-source declaration block.**

> **D-S217-Q5-1 cfb-v3-004 multi-token posture at v0.1.** Multi-token allowlist for cfb-v3-004 (harp under Llama tokenizer; first-token-proxy carry-forward) is **DECLARED at runbook v0.1** with explicit `RE-EVALUATE AT TRIAL 0` flag. At Block B Cell 13 trial 0 against ROME's single-fact dispatch, the operator empirically tests whether ROME natively handles multi-token target_new — if so, the first-token-proxy is RETIRED at v0.2; if not, first-token-proxy is RATIFIED for Block C 15-trial loop.

---

## Cell 7 — Pre-edit baseline capture (38 probes; target_TRUE natural top-1)

**Specialist:** validation-contract-architect (probe protocol; calibration-band stratification per D-S213C-CALIB-1/2/3)

**Purpose:** Capture pre-edit `P[target_new]` and `P[target_TRUE]` (natural top-1) per fact; capture all 38 active probe top-1 + p_top_1 for post-edit / post-unmount comparison. **INHERITED UNCHANGED from `stage_1_sect_runbook_v1_6.md` Cell 7.**

**Cross-session bit-exact gate:** the captured probe panel MUST match `stage_1_llama_baselines.json` at `0.00e+00` drift; drift > 0 = session-level halt per D-S217-4.

---

## Cell 8 — R1.3-equivalent dry-run gate for ROME dispatch path

**Specialist:** memit-specialist (ROME dispatch surface) + state-consistency-theorist (cache-dispatch round-trip)

**Purpose:** Pre-Block-B cache-dispatch defect-class detection under the ROME edit invocation path. Adapts `stage_1_sect_runbook_v1_6.md` § §1.5.1 D-S28-2 R1.3 codification to ROME — invokes ROME's `apply_rome_to_model` (or equivalent) on a `_ConfigOnlyPlaceholder` model with a single dummy fact at L17 to verify `get_cov` resolves to the cached `_t100_` form without local recompute. Per C-ROME-3.

```python
# === CELL 8 — R1.3-equivalent dry-run gate (ROME) ===
# Specialist: memit-specialist + state-consistency-theorist
# References: rome-patches-canonical.md v0.1 §4.3 C-ROME-3;
#             D-S28-2 R1.3 codification (carry-forward from stage_1_sect_runbook_v1_6.md §1.5.1)

import time, io, contextlib

# v0.1 R1.3-equivalent: invoke ROME's get_cov through apply_rome_to_model on a placeholder
# model with the L17 hparams + cfb-v3-001 dummy request. Capture stdout to detect
# "Computing Cov locally" log line (the canonical local-recompute signature from
# rome/layer_stats.py post-P-5 dataset loader).
#
# v0.1 NOTE: this cell is DECLARATIVE at S2.17 authoring time. Empirical first-execution
# at S2.18 produces the verdict; v0.2 absorbs implementation-specific dispatch details.
# The high-level binding: dispatch path through apply_rome_to_model → get_cov MUST
# resolve to "Loading cached covariance for layer 17" log line (or equivalent) within
# < 30 sec. Local recompute = halt.

from rome import apply_rome_to_model    # v0.1 placeholder import; verify at first execution
# ... [v0.1 declarative; cell body materializes at S2.18 Block A first execution]

# At v0.1, the cell body is reserved for empirical authoring. The operator
# at S2.18 first execution adapts the MEMIT R1.3 pattern (Cell 3 §3.8 of
# stage_1_sect_runbook_v1_6.md) to ROME's apply_rome_to_model entrypoint
# and captures the smoke-load timing.

R1_3_TIMEOUT_SEC = 30
print(f"Cell 8: R1.3-equivalent dry-run gate AUTHORED v0.1 (declarative); empirical execution at S2.18 first run.")
print(f"  Expected: 'Loading cached covariance for layer 17' log line within {R1_3_TIMEOUT_SEC} sec.")
print(f"  Halt condition: 'Computing Cov locally' log line OR > {R1_3_TIMEOUT_SEC} sec timeout.")
```

**Verification anchors (declarative at v0.1):**

| Anchor | Expected |
|---|---|
| ROME `get_cov` resolution log line | `Loading cached covariance for layer 17` (or `2` for Layer-B test) |
| Smoke-load wall-time | < 30 sec |
| Local recompute log line | ABSENT |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `Computing Cov locally` log line | Session-level | Hard halt — cache-dispatch round-trip broken; verify `rome/layer_stats.py` post-P-6 form via Cell 2 re-run; investigate ROME `get_cov` invocation path |
| Smoke-load wall-time > 30 sec | Session-level | Hard halt — same as above |
| `apply_rome_to_model` import failure | Pre-flight | Re-verify `os.chdir(ROME_ROOT)` per C-S25-5-equivalent; re-verify Cell 2 patch state |

> **v0.1 ratification note.** The cell body for R1.3-equivalent under ROME is declarative at v0.1; v0.2 absorbs the empirical first-execution implementation per C-ROME-3 (no v0.x → v0.(x+1) advance without R1.3-equivalent dry-run gate verification).

---

# Part IV — Block B: HC-2-equivalent dry-run (Cells 9–13)

> **Block B purpose.** ROME's natural test surface is a single edit at a single layer. Block B is a controlled pilot that validates the full ROME dispatch path on one fact (cfb-v3-001 guitar — the sharpest IN-BAND anchor per S2.13-C calibration) at one layer at a time before committing to Block C's 15-trial 5-fact protocol.
>
> **Cross-layer comparison rationale.** L17 (ROME paper precedent for transformer-mid on GPT-J / GPT-2-XL) gives us the published-mechanism precedent on a different target architecture; L2 (S2.14-D D.1 mediation peak) gives us the Llama-3.1-8B-specific causal mediation evidence. Cross-layer comparison at Cell 12 is the load-bearing surface for Block C layer selection.

## Cell 9 — Single edit dispatch: cfb-v3-001 guitar at Layer-A (L17 primary)

**Specialist:** memit-specialist (ROME dispatch) + validation-contract-architect (verdict surface)

**Purpose:** Apply ROME edit on cfb-v3-001 (Bo Jackson plays the instrument of guitar) at L17. Capture pre-edit / post-edit / post-unmount probe panels.

```python
# === CELL 9 — Single edit dispatch: cfb-v3-001 at Layer-A (L17 primary) ===
# Specialist: memit-specialist + validation-contract-architect
# References: D-S217-Q4-1 (Layer-A primary = L17 ROME paper precedent);
#             rome-patches-canonical.md v0.1 §3.2 layer-set candidates;
#             cfb-v3.yaml v1.0; probe-set-v3.yaml v1.0

# Single-fact ROME request (cfb-v3-001)
rome_request_l17 = {
    "prompt": "{} plays the instrument of",
    "subject": "Bo Jackson",
    "target_new": {"str": "guitar"},
}

# Pre-edit probe panel capture (38 active probes)
# ... [carry-forward implementation from stage_1_sect_runbook_v1_6.md Cell 9 trial fn body]
# ... [adapted to single-fact ROME: pre-edit P → apply_rome_to_model → post-edit P → Copy-Unmount → post-unmount P]

# At v0.1 the dispatch surface is:
#   from rome import apply_rome_to_model
#   model_edited, weights_copy = apply_rome_to_model(
#       model, tokenizer, [rome_request_l17],
#       hparams=ROME_HPARAMS_LAYER_A, copy=False, return_orig_weights=True
#   )
# `weights_copy` is the original weight tensor for L17.mlp.down_proj; used at Copy-Unmount.

# v0.1 placeholder (full implementation at S2.18 Block B first execution):
print("Cell 9: HC-2-equivalent dry-run at Layer-A=L17 — declarative at v0.1.")
print("  Materializes at S2.18 Block B first execution per t2_rome_runbook_v0_1_authoring_plan.md §6 acceptance criterion 5.")
```

**Verification anchors (declarative; resolved at S2.18):**

| Anchor | Expected |
|---|---|
| Pre-edit `P(target_new=guitar)` | Cell 7 captured baseline |
| Post-edit `P(target_new=guitar)` | > 0.5 (consistency band) — empirical at S2.18 |
| Post-edit top-1 token | guitar — empirical at S2.18 |
| Post-unmount `abs(P(target_TRUE) - pre)` | < 1e-4 (HARD per IC-S23-4) |
| Generalization probes drift | < 0.05 per probe |
| Shared specificity probes drift | < 0.05 per probe |

**Halt conditions:** Unmount band drift > 1e-4 = immediate halt per IC-S23-4.

---

## Cell 10 — Verdict surface for Cell 9 (Layer-A L17)

**Specialist:** validation-contract-architect

**Purpose:** Compute consistency / generalization / specificity / unmount verdicts for the Layer-A L17 single-fact dispatch. Write `t2_rome_block_b_layer_a_verdict.json`.

> **v0.1 implementation:** carry-forward from `stage_1_sect_runbook_v1_6.md` Cell 9's per-trial verdict computation, adapted to single-fact (1 fact instead of 5; per-trial probe count = 17 per `stage_1_sect_runbook_v1_6.md` §12.2 v3 38-probe roster).

---

## Cell 11 — Single edit dispatch: cfb-v3-001 guitar at Layer-B (L2 secondary)

**Specialist:** memit-specialist (ROME dispatch) + validation-contract-architect (verdict surface)

**Purpose:** Apply ROME edit on cfb-v3-001 at L2. Same dispatch surface as Cell 9 with `ROME_HPARAMS_LAYER_B` (L2). **Pre-execution requires Copy-Unmount restore from Cell 9 first** — the Cell 9 edit must be fully unmounted before Cell 11 dispatch to ensure the L2 test runs against pristine model state.

> **Implementation note.** v0.1 declarative; full body at S2.18 Block B first execution.

---

## Cell 12 — Verdict surface for Cell 11 (Layer-B L2) + cross-layer comparison

**Specialist:** validation-contract-architect

**Purpose:** Compute Layer-B L2 verdicts (parallel to Cell 10); compute cross-layer comparison metrics. Write `t2_rome_block_b_layer_b_verdict.json` + `t2_rome_block_b_cross_layer_comparison.json`.

**Cross-layer comparison metrics:**

| Metric | Layer-A (L17) | Layer-B (L2) | Comparison verdict |
|---|---|---|---|
| Post-edit `P(target_new)` | <empirical> | <empirical> | Higher → load-bearing layer candidate |
| Generalization drift (avg) | <empirical> | <empirical> | Lower → load-bearing layer candidate |
| Shared spec drift (avg) | <empirical> | <empirical> | Lower → load-bearing layer candidate |
| Unmount drift (HARD gate) | <empirical> | <empirical> | Both must PASS < 1e-4 |
| Wall-time | <empirical> | <empirical> | Lower → operational preference |

---

## Cell 13 — Block B verdict gate: load-bearing layer selection + multi-token finalization

**Specialist:** validation-contract-architect (verdict gate authority) + memit-specialist (mechanism interpretation)

**Purpose:** Block B verdict consolidation. Three deliverables:

1. **Load-bearing layer for Block C selected** — the Cell 12 cross-layer comparison verdict picks ONE of {L17, L2} as the load-bearing layer. Block C 15-trial loop runs at this layer only.
2. **Multi-token tolerance posture for cfb-v3-004 finalized** — the Cell 9 / 11 trials at Layer-A and Layer-B run on cfb-v3-001 (single-token target_new "guitar"); cfb-v3-004 multi-token is empirically tested at this gate (Cell 13). If ROME's `apply_rome_to_model` natively handles multi-token target_new, first-token-proxy is RETIRED for Block C; if not, first-token-proxy is RATIFIED. Closes OQ-S217-1 (carry-forward of OQ-S216-4) at Trial 0.
3. **OQ-S216-2 partial-resolution → full-resolution** — ROME canonical hparams calibrated against empirical Block B results. v_lr / v_num_grad_steps / mom2_adjustment may be adjusted based on Block B observed dynamics; full hparam set finalized at this gate.

**Verdict classes:**

| Block B verdict class | Definition | Routes to |
|---|---|---|
| **B-PASS** | At least one of {L17, L2} produces in-band edit (consistency > 0.5) AND unmount band PASS at < 1e-4 AND multi-token resolution finalized | Block C 15-trial execution at the load-bearing layer |
| **B-FAIL** | Both layer candidates FAIL the calibration corridor (consistency ≤ 0.5 at both AND/OR unmount band FAIL at either) | Escalate to D-S216-Q3-1 path: GRACE adapter-based mechanism (S2.19 = T.2 GRACE runbook authoring; S2.20 = GRACE execution) |
| **B-PARTIAL** | One layer PASSES consistency band but unmount FAILS, OR consistency band borderline (between 0.4 and 0.5) | Operator-side verdict integrity binding re-evaluation (per `t_branch_decision_document.md` §5 conditional execution plan) |

> **v0.1 declarative anchor:** verdict computation logic at v0.1 is structurally declared; numerical thresholds (consistency 0.5; unmount 1e-4) inherit from D-S24-10 + IC-S23-4 carry-forward. Empirical instantiation at S2.18 Block B Cell 13 first execution.

---

# Part V — Block C: Stage 1 SECT v3 execution at single-fact ROME dispatch (Cells 14–20)

> **Block C purpose.** Execute the 15-trial Stage 1 SECT v3 protocol per IC-S24-4 against the load-bearing layer selected at Block B Cell 13. Each trial is a single-fact ROME edit (per C-ROME-1). Trial loop structure mirrors `stage_1_sect_runbook_v1_6.md` Block VII (Cells 8–10) with the single-fact dispatch narrowing.

## Cell 14 — Trial matrix authoring (D-S217-2 + verdict integrity binding carry-forward)

**Specialist:** validation-contract-architect (IC-S24-4 enforcement)

**Purpose:** Enumerate the 15 trials per IC-S24-4 (5 facts × 3 replicates); apply D-S217-2 cross-cell SUBSET hard gate (Cell 6 ↔ Cell 8 ↔ Cell 14 single-source); apply D-S215D2-VERDICT-INTEGRITY-1 load-bearing-subset annotation.

> **Carry-forward from MEMIT runbook v1.6 Cell 8.** The trial matrix authoring logic is structurally identical to MEMIT runbook v1.6 Cell 8, with three ROME-specific adjustments:
>
> 1. **Per-trial probe count is 17** (per stage_1_sect_runbook_v1_6.md §12.2 v3 roster; same as MEMIT v3).
> 2. **Per-fact ROME hparams** select the Block-B-elected load-bearing layer (single-fact narrowing).
> 3. **D-S215D2-VERDICT-INTEGRITY-1 load-bearing subset** = {cfb-v3-001, cfb-v3-002, cfb-v3-005}; forensic-informative-excluded by default = {cfb-v3-003, cfb-v3-004} modulo Block B Cell 13 cfb-v3-004 reclassification per Q5 / OQ-S217-1.

```python
# === CELL 14 — Trial matrix authoring (single-fact ROME dispatch) ===
# Specialist: validation-contract-architect
# References: IC-S24-4 (5×3 trial protocol); D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset);
#             D-S217-Q4-1 (load-bearing layer from Block B Cell 13);
#             D-S217-2 (Cell 6/8 single-source contract; carry-forward to Cell 14)

LOAD_BEARING_LAYER = block_b_verdict["load_bearing_layer"]  # from Cell 13: 17 OR 2
ROME_HPARAMS_BLOCK_C = ROME_HPARAMS_LAYER_A if LOAD_BEARING_LAYER == 17 else ROME_HPARAMS_LAYER_B

# Carry-forward from MEMIT runbook v1.6 Cell 8 (D-S217-2 cross-cell SUBSET gate inherited)
# fact_memit_requests is the canonical source per D-S217-2 — under ROME, the request schema
# is single-fact (no batched dispatch per C-ROME-1). The Cell 6 stage_1_facts and Cell 8
# fact_memit_requests have been verified equivalent at the Cell 8 D-S217-2 gate.

# Verdict integrity binding: per-fact subset annotation for D-S215D2-VERDICT-INTEGRITY-1 carry-forward
LOAD_BEARING_SUBSET = {"cfb-v3-001", "cfb-v3-002", "cfb-v3-005"}
FORENSIC_INFORMATIVE_DEFAULT = {"cfb-v3-003", "cfb-v3-004"}  # cfb-v3-004 reclassified per Cell 13 Q5 outcome

trial_matrix = []
trial_index = 0
for fact_id in stage_1_eligible_facts:
    for replicate in range(1, REPLICATES + 1):
        trial_matrix.append({
            "trial_index": trial_index,
            "fact_id": fact_id,
            "replicate": replicate,
            "rome_request": fact_memit_requests[fact_id],   # single-fact dispatch
            "hparams_layer": LOAD_BEARING_LAYER,
            "per_fact_probes": fact_probes[fact_id],
            "shared_specificity_probes": shared_specificity_probes,
            "torch_seed": 0,
            "subset_annotation": (
                "load_bearing" if fact_id in LOAD_BEARING_SUBSET
                else "forensic_informative_excluded"
            ),
        })
        trial_index += 1

assert len(trial_matrix) == 15, f"Trial count mismatch: {len(trial_matrix)}"

# ... [carry-forward C-S24-7 hard gate from MEMIT v1.6 Cell 8]
# ... [carry-forward write to /workspace/t2_rome_sect/trial_matrix.json]
```

---

## Cell 15 — Trial loop execution (single-fact ROME edits + Copy-Unmount per fact)

**Specialist:** memit-specialist (ROME dispatch) + state-consistency-theorist (Copy-Unmount integrity) + validation-contract-architect (verdict computation)

**Purpose:** Execute the 15-trial loop. Each trial: pre-edit probe panel → ROME single-fact edit at LOAD_BEARING_LAYER → post-edit probe panel → Copy-Unmount → post-unmount probe panel. Per-trial JSON write + per-trial overlay snapshot.

> **Carry-forward from MEMIT runbook v1.6 Cell 9.** The trial loop structure is structurally identical to MEMIT runbook v1.6 Cell 9, with these ROME-specific adjustments:
>
> 1. **Single-fact dispatch:** `apply_rome_to_model` invoked with a list of one request per trial (not five).
> 2. **Copy-Unmount narrowing:** restore is single-layer (LOAD_BEARING_LAYER) per fact, not 5 layers; structurally narrower regime than the L4-L8 / L2-L6 anchors validated at S2.14-D D.3 / S2.15-D2.
> 3. **Per-trial overlay snapshot:** ~16 MB FP16 per single layer (not ~80 MB for 5-layer); 30 .pt files total at Block C close.
> 4. **`return_orig_weights=True`** on `apply_rome_to_model` provides the unmount handle directly — no manual `state_dict().clone()` step needed (mechanism preserved; invocation surface differs from MEMIT's manual snapshot).
> 5. **Inter-trial baseline drift gate:** preserved unchanged — per IC-S23-4, inter-trial drift on shared-spec probes < 1e-4 (HARD); halt at violation.
> 6. **Unmount band gate:** preserved unchanged — per IC-S23-4, post-unmount drift on `target_TRUE` < 1e-4 (HARD); halt at violation.

```python
# === CELL 15 — Trial loop execution (single-fact ROME dispatch) ===
# Specialist: memit-specialist + state-consistency-theorist + validation-contract-architect
# References: IC-S24-4; IC-S23-4 (unmount band); C-S24-8; D-S215D2-VERDICT-INTEGRITY-1;
#             stage_1_sect_runbook_v1_6.md Cell 9 (carry-forward structural template)

from rome import apply_rome_to_model

def run_trial(trial):
    # ... [pre-edit probe panel capture]
    # ... [inter-trial baseline drift gate (per IC-S23-4)]

    # ROME single-fact dispatch
    model_edited, weights_copy = apply_rome_to_model(
        model, tokenizer,
        [trial["rome_request"]],                 # single-fact list
        hparams=ROME_HPARAMS_BLOCK_C,
        copy=False,
        return_orig_weights=True
    )

    # ... [post-edit probe panel capture]

    # Copy-Unmount: restore single layer in-place
    layer_module_name = f"model.layers.{LOAD_BEARING_LAYER}.mlp.down_proj"
    with torch.no_grad():
        model.state_dict()[f"{layer_module_name}.weight"].copy_(
            weights_copy[f"{layer_module_name}.weight"]
        )

    # ... [post-unmount probe panel capture]
    # ... [unmount band gate (per IC-S23-4) — HARD halt on violation]
    # ... [verdict computation: consistency / generalization / specificity / unmount]
    # ... [per-trial JSON write to /workspace/t2_rome_sect/trials/]
    # ... [overlay snapshot write: edited.pt + original.pt for the single layer]

    return trial_verdict

# Trial loop with halt-class enforcement
for trial in trial_matrix:
    verdict = run_trial(trial)
    if verdict["unmount_band_status"] == "FAIL":
        raise RuntimeError(f"Unmount band HARD halt at trial {trial['trial_index']}")
```

**Per-trial verdict schema** (parallel to MEMIT v1.6 Cell 9 per-trial JSON; ROME-specific keys):

```json
{
  "trial_index": <int 0-14>,
  "fact_id": "cfb-v3-XXX",
  "replicate": <int 1-3>,
  "subset_annotation": "load_bearing|forensic_informative_excluded",
  "rome_request": {...},
  "hparams_layer": <17|2>,
  "wall_time_sec": <float>,
  "consistency": {"p_target_new_post": <float>, "top_1_post": <str>, "verdict": "PASS|FAIL"},
  "generalization": {"per_probe_drift": [...], "verdict": "PASS|FAIL"},
  "specificity_shared": {"per_probe_drift": [...], "verdict": "PASS|FAIL"},
  "unmount_band": {"abs_drift_target_true": <float>, "verdict": "PASS|FAIL", "_HARD": true},
  "rome_specific": {
    "v_loss_at_step_final": <float>,
    "v_norm_clip_factor_used": <float>,
    "weights_copy_layer_sha_prefix": <str>
  }
}
```

---

## Cell 16 — Per-trial verdict aggregation

**Specialist:** validation-contract-architect

**Purpose:** Aggregate per-trial verdicts into per-fact and full-aggregate views. **INHERITED from `stage_1_sect_runbook_v1_6.md` Cell 10** with cell-numbering shift.

---

## Cell 17 — Aggregate verdict (load-bearing subset + full-aggregate)

**Specialist:** validation-contract-architect (verdict integrity binding authority)

**Purpose:** Compute the load-bearing-subset aggregate (decisive per D-S215D2-VERDICT-INTEGRITY-1) AND the full 5-fact aggregate (informational). Write `t2_rome_aggregate_verdict.json`.

**Verdict classes for Block C:**

| Verdict | Definition | Routes to (per `t_branch_decision_document.md` §5) |
|---|---|---|
| **C-PASS** | Load-bearing subset {cfb-v3-001, cfb-v3-002, cfb-v3-005}: ≥ 2 of 3 facts at ≥ 2/3 trials each PASS consistency AND all 15 trials PASS unmount band | T.2 ROME PASS → S2.19 = MEMIT-vs-ROME comparison framework finding update (resolves OQ-S216-6) |
| **C-FAIL** | Load-bearing subset FAIL OR any trial FAILS unmount band | T.2 ROME FAIL → S2.19 = T.2 GRACE runbook authoring; S2.20 = GRACE execution |
| **C-PARTIAL** | Load-bearing subset borderline: 2/3 facts PASS but < 2/3 trials each, OR sentinel-FAIL ambiguity | Operator-side verdict integrity binding re-evaluation per `t_branch_decision_document.md` §5 conditional execution plan |

---

## Cell 18 — NV inventory + SHA equality gate

**Specialist:** state-consistency-theorist

**Purpose:** Verify all per-trial JSONs, overlay snapshots, and aggregate verdict are written to NV at canonical paths. Run SHA equality gate (cache_state.provenance.model_revision_sha vs env_fingerprint.model_revision_sha) per OQ-S28-4 carry-forward / v1.6 try-both fallback. Write `t2_rome_nv_inventory.json`.

> **Carry-forward from MEMIT runbook v1.6 Cell 11.** Adapted: NV_TARGETS path prefix is `/workspace/t2_rome_sect/` instead of `/workspace/stage_1_sect/`; OVERLAY_TARGETS file count is 30 (15 trials × 2 files: `edited.pt` + `original.pt` per single layer at Copy-Unmount snapshot).

---

## Cell 19 — Mirror sync (NV → SSD)

**Specialist:** state-consistency-theorist

**Purpose:** rsync NV `/workspace/t2_rome_sect/` to SSD mirror. Pattern carries forward from S2.15-D2 close (4-command rsync mirror discipline). Write `t2_rome_mirror_sync.log`.

---

## Cell 20 — Block C verdict + reproducibility manifest update

**Specialist:** state-consistency-theorist (manifest discipline)

**Purpose:** Append S2.18 execution state to `/workspace/reproducibility_manifest.json` (`sessions["2.18"]`). Print Block C verdict class. Print routing decision per `t_branch_decision_document.md` §5.

> **Carry-forward from MEMIT runbook v1.6 Cell 12.** Adapted: SESSION_LABEL="S2.18"; NV-resident artifact paths under `/workspace/t2_rome_sect/`.

---

# Part VI — Halt conditions (cross-cell index)

See § §1.4 above for the full halt-condition index.

---

# Part VII — Forward routing (S2.19 prep)

| Block C verdict | Successor session | Successor scope |
|---|---|---|
| C-PASS | S2.19 | MEMIT-vs-ROME comparison framework finding update; resolves OQ-S216-6 |
| C-FAIL | S2.19 | T.2 GRACE runbook v0.1 authoring; S2.20 = GRACE execution |
| C-PARTIAL | S2.19 (re-evaluation) | Operator-side verdict integrity binding re-evaluation per `t_branch_decision_document.md` §5 |

---

# Part VIII — Open questions in scope

## 8.1 OQs closed by this runbook's execution at S2.18

| OQ ID | Closure mechanism |
|---|---|
| **OQ-S216-1** | Cell 1 ROME SHA pin resolution at first execution |
| **OQ-S216-2** | Cell 13 Block B verdict gate; full hparam calibration |
| **OQ-S216-3** | Cell 13 Block B verdict gate; load-bearing layer selection |
| **OQ-S216-4** (= OQ-S217-1) | Cell 13 Block B verdict gate; cfb-v3-004 multi-token tolerance posture finalization |

## 8.2 OQs activated / opened at this runbook authoring (v0.1)

| OQ ID | Surface |
|---|---|
| **OQ-S217-2** | L17 covariance cache availability — extend cache OR restrict layer candidate. Operator-side resolution at S2.18 Block A entry, before pod attach. Recommended: extend cache to include L17 |
| **OQ-S217-3** | ROME `apply_rome_to_model` invocation API matches v0.1 declared schema (positional + keyword args). Verified at Cell 8 R1.3-equivalent dry-run gate / Cell 9 first dispatch |
| **OQ-S217-4** | ROME multi-token target_new native handling (resolves Q5 finalization) — deferred to Block B Cell 13 trial 0 |

## 8.3 OQs explicitly out of scope for this runbook

| OQ ID | Reason |
|---|---|
| OQ-S216-5 | v1.6 hardening session scheduling — closed at S2.16 / S2.17 Block 1 |
| OQ-S216-6 | MEMIT-vs-ROME comparison framework finding update — out of v0.1 runbook scope; deferred to S2.19 post-Block-C verdict |

---

# Part IX — Non-goals

This runbook v0.1 does NOT:

1. **Modify `memit-patches-canonical.md` v2.5.** Preserved per D-S216-CLOSE-3.
2. **Modify `stage_1_sect_runbook_v1_6.md`.** Preserved post-S2.17 Block 1 ratification; this runbook structurally inherits.
3. **Pre-commit empirical patch applicability.** `rome-patches-canonical.md` v0.1 §1 verdicts are declared; empirical at S2.18 Block A Cell 2.
4. **Pre-commit ROME hparam values for Block C.** Cell 4 declares paper Table 1 GPT-J reference values; calibrated at Block B Cell 13.
5. **Pre-commit Block C verdict.** Empirical at S2.18 Block C Cell 17.
6. **Author runtime implementation code beyond declarative scaffolding.** v0.1 cell bodies are structurally complete but empirically declarative; v0.2 absorbs first-execution implementation specifics.
7. **Amend the v1.2 integrated framework spec.** Sealed.

---

# Part X — Reference appendices

## 10.1 Carry-forward inheritance from `stage_1_sect_runbook_v1_6.md`

| Component | Inherited unchanged | Adapted | NEW for ROME |
|---|---|---|---|
| Cell 0 (pod + deps) | ✓ | | |
| Cell 1 (env fingerprint) | | ✓ (rome_sha extension) | |
| Cell 1.5 (manifest write) | ✓ (EXPECTED_KEYS extended) | | |
| Cell 2 (patch state) | | ✓ (6-marker subset; P-7 omitted) | |
| Cell 3 (cache provenance + SUBSET assertion) | ✓ (v1.6 SUBSET pattern) | | |
| Cell 4 (hparams) | | ✓ (ROME schema; 2-layer candidate dict) | |
| Cell 5 (model load + Pad-Token + bit-exact gate) | ✓ | | |
| Cell 6 (tokenizer single-token; D-S217-2 single-source) | ✓ | | |
| Cell 7 (baseline + target_TRUE; calibration-band stratification) | ✓ | | |
| Cell 8 (R1.3-equivalent dry-run gate) | | ✓ (ROME dispatch surface) | |
| Cells 9-13 (Block B HC-2-equivalent dry-run) | | | ✓ (5 cells) |
| Cell 14 (trial matrix; D-S217-2 + verdict integrity binding) | ✓ | | |
| Cell 15 (trial loop) | | ✓ (single-fact ROME dispatch; Copy-Unmount narrowing) | |
| Cells 16-20 (verdict aggregation + persistence) | ✓ (cell-numbering shift) | | |

## 10.2 NV-resident artifact paths (final state at S2.18 close)

```
/workspace/architecture_profile/
  ├── meta-llama_Llama-3.1-8B.json                      (S2.5a; consumed by Cell 4)
  ├── stage_1_environment_fingerprint.json              (MEMIT runbook fingerprint; preserved)
  ├── t2_rome_environment_fingerprint.json              (Cell 1.5 output; ROME fingerprint)
  ├── t2_rome_pinned_sha.txt                            (Cell 1 output; ROME SHA pin)
  ├── t2_rome_patch_state.json                          (Cell 2 output)
  ├── t2_rome_cache_state.json                          (Cell 3 output; v1.6 "provenance" key)
  ├── t2_rome_hparams.json                              (Cell 4 output; 2-layer dict)
  ├── stage_1_token_verification.json                   (Cell 6 output; same as MEMIT runbook)
  └── stage_1_llama_baselines.json                      (Cell 7 output; same 38-probe baseline)

/workspace/rome_dry_run/rome/                           (Cell 1 NEW — ROME repo clone)

/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/
  ├── PROVENANCE.txt                                    (pre-S2.6 fork-work; consumed by Cell 3)
  └── (≥ 7 cache files; SUBSET-superset acceptable per D-S215D2-CELL3-SUBSET-ASSERTION-1
       MUST include L17 + L2 covariance for Block B / Block C — operator-side cache extension at OQ-S217-2)

/workspace/t2_rome_sect/
  ├── block_b_layer_a_verdict.json                      (Cell 10 output)
  ├── block_b_layer_b_verdict.json                      (Cell 12 output)
  ├── block_b_cross_layer_comparison.json               (Cell 12 output)
  ├── block_b_verdict_gate.json                         (Cell 13 output; load-bearing layer selected)
  ├── trial_matrix.json                                 (Cell 14 output; 15 trials)
  ├── trials/
  │   └── (15 per-trial JSONs at t2_rome_trial_cfb-v3-XXX_rN.json)
  ├── overlays/
  │   └── (15 dirs × 2 files = 30 .pt files; single-layer Copy-Unmount snapshots)
  ├── trial_loop_log.json                               (Cell 15 consolidated)
  ├── aggregate_verdict.json                            (Cell 17 — Block C verdict)
  ├── nv_inventory.json                                 (Cell 18 output; SHA equality gate)
  └── mirror_sync.log                                   (Cell 19 output)

/workspace/reproducibility_manifest.json                (Cell 20 update; sessions["2.18"])
```

## 10.3 Wall-time budget per cell (estimate; v0.1 declarative)

| Cell | Wall time | Notes |
|---|---|---|
| Cell 0 | ~5–8 min | dep install + kernel restart (carry-forward MEMIT v1.6) |
| Cell 1 | ~30 sec | ROME repo clone (fresh) OR SHA verification (subsequent) |
| Cell 1.5 | ~10 sec | env fingerprint write |
| Cell 2 | ~30 sec | patch verification (6 markers) |
| Cell 3 | ~1–2 min | cache SUBSET gate + R1.2 + R1.3-equivalent (cold ~30 sec; warm ~3 sec) |
| Cell 4 | ~10 sec | hparam declaration |
| Cell 5 | ~2–4 min | model load from NV-cached HF (~16 GB) |
| Cell 6 | ~30 sec | tokenizer single-token verification |
| Cell 7 | ~3–5 min | 38 forward passes + per-fact baseline + target_TRUE natural top-1 |
| Cell 8 | ~30 sec | R1.3-equivalent dry-run gate |
| **Block A subtotal** | **~13–20 min** | |
| Cell 9 | ~5–7 min | single edit dispatch L17 (ROME edit ~3–5 min + probe panel) |
| Cell 10 | ~10 sec | verdict computation |
| Cell 11 | ~5–7 min | single edit dispatch L2 |
| Cell 12 | ~10 sec | verdict computation + cross-layer comparison |
| Cell 13 | ~30 sec | Block B verdict gate |
| **Block B subtotal** | **~11–15 min** | |
| Cell 14 | ~10 sec | trial matrix authoring |
| Cell 15 | ~75–105 min | 15 trials × ~5–7 min (ROME edit ~3–5 min + probe panel + Copy-Unmount per trial) |
| Cell 16 | ~10 sec | per-trial aggregation |
| Cell 17 | ~10 sec | load-bearing subset + full aggregate verdicts |
| Cell 18 | ~30 sec | NV inventory + SHA equality gate |
| Cell 19 | ~30 sec | mirror sync NV → SSD |
| Cell 20 | ~10 sec | manifest update |
| **Block C subtotal** | **~77–108 min** | |
| **Total** | **~101–143 min** | within OQ-S25-2 envelope; comparable to MEMIT v3 5×3 expansion |

## 10.4 Cell-to-decision traceability

| Decision | Cell of realization |
|---|---|
| C-S25-5 (cwd invariant; ROME-adapted as ROME_ROOT) | Cell 2 `os.chdir(ROME_ROOT)` |
| C-ROME-1 (single-fact dispatch envelope) | Cell 14 trial matrix; Cell 15 trial loop |
| C-ROME-2 (covariance cache reuse) | Cell 3 SUBSET gate |
| C-ROME-3 (R1.3-equivalent dry-run) | Cell 8 |
| C-ROME-4 (marker post-application verification, declared) | (no v0.1 markers introduced; constraint declared at rome-patches-canonical.md v0.1 §4.4) |
| D-S217-1 (Cell 2 = canonical marker site, carry-forward) | Cell 2 |
| D-S217-2 (Cell 6/8 single-source contract, carry-forward) | Cell 6 entry block; Cell 8 cross-cell SUBSET gate; Cell 14 trial matrix |
| D-S217-3 (single-fact dispatch envelope) | § §1.5.1; Cells 14, 15 |
| D-S217-4 (empirical anchor inheritance) | § §1.5.2; Cells 5, 7 cross-session bit-exact gate |
| D-S217-Q2-1 (ROME SHA pin = latest stable tip) | Cell 1 |
| D-S217-Q3-1 (ROME hparams = paper Table 1 GPT-J) | Cell 4 |
| D-S217-Q4-1 (Layer-A=L17 + Layer-B=L2) | Cell 4 (both hparam dicts); Block B Cells 9-13 |
| D-S217-Q5-1 (cfb-v3-004 first-token-proxy + RE-EVALUATE flag) | Cell 6 (carry-forward); Cell 13 (Q5 finalization gate) |
| IC-S23-4 (intra-pod drift band 1e-4) | Cell 15 unmount band gate |
| IC-S24-4 (Stage 1 trial protocol) | Cells 14 + 15 |
| IC-S25-3 (LLaMA baseline re-capture contract) | Cell 7 |
| D-S213C-CALIB-1/2/3 (calibration-band stratification) | Cell 7 |
| D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset binding) | Cell 14 subset_annotation; Cell 17 aggregate verdict |
| D-S215D2-CELL3-SUBSET-ASSERTION-1 (cache truth ⊇ PROVENANCE) | Cell 3 |
| D-S215D2-CFB-V3-004-PROXY-1 (first-token-proxy) | Cell 6 (carry-forward) |

---

## 10.5 Authoring metadata

| Field | Value |
|---|---|
| Authoring session | S2.17 Block 2 |
| Authoring date | 2026-05-04 |
| Document version | 0.1 |
| Iteration | v1 first synthesis |
| Status | RATIFIED v0.1 — declarative; empirical instantiation at S2.18 |
| Supersedes | — |
| Basis | `stage_1_sect_runbook_v1_6.md` (structural template); `rome-patches-canonical.md` v0.1 (patches reference); `t2_rome_runbook_v0_1_authoring_plan.md` v1.0 (scoping); `t_branch_decision_document.md` (decision rationale) |
| Specialist provenance | framework-spec-writer (primary, runbook authoring); memit-specialist (Cells 1, 2, 4, 8, 9, 11, 15 — ROME mechanism); state-consistency-theorist (Cells 3, 15 — covariance cache reuse + Copy-Unmount); validation-contract-architect (Cells 6, 7, 10, 12, 13, 16 — verdict surface) |
| Last updated | 2026-05-04 |

---

*End of T.2 ROME Runbook v0.1 — RATIFIED at S2.17 Block 2 close (declarative; empirical instantiation at S2.18; v0.2 absorbs first-execution implementation specifics + Block B Cell 13 hparam calibration verdict).*
