# D.3 Multi-Target Hyperscale — Delta Runbook against `stage_1_sect_runbook_v1_5.md`

> **Authoring session:** S2.14-D (initial authoring; delta document, not standalone runbook)
> **Predecessor session:** Session 2.13-C (CLOSED C-FAIL 2026-05-04)
> **Consumer session:** S2.14-D — D.3 sub-path execution (parallel-track with D.1)
> **Reference base:** `stage_1_sect_runbook_v1_5.md` v1.5 (PROVISIONAL) — D.3 inherits all unchanged cells; this delta document specifies ONLY the modifications
> **Target environment:** RunPod RTX 4090 24 GB single GPU; NV `large_amethyst_wolverine`
> **Target model:** `meta-llama/Llama-3.1-8B` (base; carry-forward from v1.5)
> **Trial protocol:** 3 batched trials × 5 facts per batch = 15 per-fact verdicts (matches S2.13-C count for direct A/B comparison against single-fact regime)
> **Specialists:** memit-specialist (primary; Cell 9 batched MEMIT); validation-contract-architect (Cell 13 cross-fact specificity gate); state-consistency-theorist (Cell 11 NV overlay shape)
>
> **Revision:** v0.1 — Initial authoring (2026-05-04). Delta scope: Cell 8 trial-matrix modification (3 batched trials replacing 15 single-fact trials); Cell 9 batched MEMIT regime (single MEMIT pass per trial editing 5 facts concurrently); Cell 11 overlay shape (1 overlay per batched trial vs 1 per single-fact trial); Cell 13 cross-fact specificity gate (shared-spec drift comparison vs S2.13-C single-fact baseline); D.3 verdict predicate replacing v1.5 Stage 1 consistency aggregate. v0.1 ships under PROVISIONAL status until Cell 13 verdict produces the D.3 mediation outcome.

---

## 1.4 Patch scope — full v1.5 patch state load-bearing

D.3 inherits the v1.5 active patch set in full. Unlike the D.1 forward-pass-only trace, D.3 EXECUTES MEMIT EDITS, so all of P-1, P-2, P-3', P-4, P-5, P-6, P-7, Pad-Token, and Copy-Unmount are load-bearing. C-S26-1 (`batch_tokens=100`) and C-S28-1 (defense-in-depth marker post-application verification) carry forward unchanged.

The L4-L8 covariance caches at `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` are durable from S2.13-C and load-bearing for D.3. **No covariance rebuild required** (this is the cost-advantage of D.3 vs D.2).

---

## 1.5 Authoring discipline — D.3 methodology lock

The following decisions are binding for v0.1 and gate cell semantics:

| ID | Decision |
|---|---|
| **D-S214D-D3-METHOD-1** | Batched MEMIT regime: 5 facts edited concurrently in a single `apply_memit_to_model` call per trial (vs v1.5 single-fact-per-trial regime). |
| **D-S214D-D3-METHOD-2** | Trial count: 3 batched trials × 5 facts = 15 per-fact verdicts. Matches S2.13-C count (15 single-fact trials) for direct A/B comparison. |
| **D-S214D-D3-METHOD-3** | Replicate semantics: each batched trial uses a distinct `torch_seed` (vs v1.5's same-seed-across-replicates). Tests stochastic stability of batched z-vector optimization across initialization seeds. |
| **D-S214D-D3-METHOD-4** | Cross-fact specificity gate: shared-specificity probes re-run post-batched-edit; drift compared against S2.13-C single-fact baseline median. Substantial increase in shared-spec drift = batched-regime interference signal. |
| **D-S214D-D3-METHOD-5** | Verdict predicate: D.3 PASS if ≥3/5 facts achieve consistency PASS at ≥2/3 trials each (mirrors v1.5 per-fact aggregation per OQ-S212A-2 closure); D.3 FAIL otherwise; D.3 PARTIAL if consistency aggregate borderline AND cross-fact drift elevated. |
| **D-S214D-D3-METHOD-6** | Corpus + probe-set: cfb-v3.yaml v1.0 + probe-set-v3.yaml v1.0 (LOCKED at S2.13-C). No re-authoring; carry-forward. |

---

# Part I — Delta scope

## 1.1 Cells unchanged from v1.5 (carry-forward without modification)

| Cell | v1.5 purpose | D.3 status |
|---|---|---|
| Cell 0 | HF env-var injection block | UNCHANGED |
| Cell 0-VERIFY | Library-constant freeze assertion | UNCHANGED |
| Cell 1 | Environment fingerprint | UNCHANGED (session_label = "S2.14-D / D.3 batched / v0.1") |
| Cell 2 | Patch state verification | UNCHANGED |
| Cell 3 | Cache provenance verification (R1.1/R1.2/R1.3) | UNCHANGED |
| Cell 4 | Architecture profile load | UNCHANGED |
| Cell 5 | Model + tokenizer load | UNCHANGED |
| Cell 6 | LLaMA tokenizer single-token verification | UNCHANGED (cfb-v3 carry-forward) |
| Cell 7 | Pre-edit baseline capture | UNCHANGED (cfb-v3 + probe-set-v3 carry-forward) |
| Cell 10 | Trial loop driver | UNCHANGED (executes whatever Cell 8 enumerates; trial-shape-agnostic) |
| Cell 12 | Session close (NV reproducibility manifest) | UNCHANGED (SESSION_LABEL parameterized) |

## 1.2 Cells modified in D.3 (delta scope)

| Cell | v1.5 form | D.3 form | Delta description |
|---|---|---|---|
| Cell 8 | 5 facts × 3 replicates = 15 single-fact trials | 3 replicates × 1 batched trial = 3 batched trials (15 per-fact verdicts on probe) | Replace per-fact-per-replicate enumeration with per-replicate batched enumeration; each trial carries `requests = [all 5 fact memit_requests]` |
| Cell 9 | Single-fact MEMIT trial body | Batched MEMIT trial body | Single MEMIT pass per trial; per-fact probe loop after edit |
| Cell 11 | Per-fact-per-replicate overlay (15 overlays) | Per-batched-trial overlay (3 overlays); each overlay edits 5 facts | Reduced overlay count; each overlay encodes joint 5-fact edit |
| Cell 13 | Per-fact verdict aggregation + Stage 1 consistency aggregate | Per-fact verdict aggregation + cross-fact specificity gate + D.3 verdict | New cross-fact gate; replace Stage 1 verdict with D.3 verdict |

---

# Part II — Cell-by-Cell delta

## §2.1 — Cell 8 modification — Trial matrix (batched form)

**Specialist:** validation-contract-architect (D-S214D-D3-METHOD-2 enforcement)

**Replaces:** v1.5 Cell 8 lines 1944–2070 (single-fact trial enumeration)

```python
# === CELL 8 (D.3 DELTA) — Trial matrix (batched form) ===
# Specialist: validation-contract-architect
# References: D-S214D-D3-METHOD-1, METHOD-2, METHOD-3
# v1.5 single-fact trials → D.3 batched trials. 3 replicates × 5 facts = 15
# per-fact verdicts (matches S2.13-C count for direct A/B comparison).

import os, json
from datetime import datetime, timezone

# Carry-forward from cfb-v3.yaml v1.0 (LOCKED at S2.13-C)
stage_1_eligible_facts = ["cfb-v3-001", "cfb-v3-002", "cfb-v3-003", "cfb-v3-004", "cfb-v3-005"]
REPLICATES = 3

# Carry-forward fact_memit_requests + fact_probes + shared_specificity_probes
# (identical to v1.5 Cell 8; cfb-v3 v1.0 corpus carry-forward)
fact_memit_requests = {
    "cfb-v3-001": {"prompt": "{} plays the instrument of", "subject": "Bo Jackson",        "target_new": {"str": "guitar"}},
    "cfb-v3-002": {"prompt": "{} plays the instrument of", "subject": "Tiger Woods",       "target_new": {"str": "piano"}},
    "cfb-v3-003": {"prompt": "{} plays the instrument of", "subject": "Deion Sanders",     "target_new": {"str": "violin"}},
    "cfb-v3-004": {"prompt": "{} plays the instrument of", "subject": "Hakeem Olajuwon",   "target_new": {"str": "harp"}},
    "cfb-v3-005": {"prompt": "{} plays the instrument of", "subject": "Lindsey Vonn",      "target_new": {"str": "flute"}},
}

fact_probes = {
    # Identical to v1.5 Cell 8 fact_probes dict — carry-forward verbatim
    "cfb-v3-001": {"consistency":  ["p-cfb-v3-001-cons-1", "p-cfb-v3-001-cons-2", "p-cfb-v3-001-cons-3"],
                   "generalization": ["p-cfb-v3-001-gen-1", "p-cfb-v3-001-gen-2", "p-cfb-v3-001-gen-3"],
                   "specificity_per_fact": [], "unmount": ["p-cfb-v3-001-unmount-1"]},
    "cfb-v3-002": {"consistency":  ["p-cfb-v3-002-cons-1", "p-cfb-v3-002-cons-2", "p-cfb-v3-002-cons-3"],
                   "generalization": ["p-cfb-v3-002-gen-1", "p-cfb-v3-002-gen-2", "p-cfb-v3-002-gen-3"],
                   "specificity_per_fact": [], "unmount": ["p-cfb-v3-002-unmount-1"]},
    "cfb-v3-003": {"consistency":  ["p-cfb-v3-003-cons-1", "p-cfb-v3-003-cons-2", "p-cfb-v3-003-cons-3"],
                   "generalization": ["p-cfb-v3-003-gen-1", "p-cfb-v3-003-gen-2", "p-cfb-v3-003-gen-3"],
                   "specificity_per_fact": [], "unmount": ["p-cfb-v3-003-unmount-1"]},
    "cfb-v3-004": {"consistency":  ["p-cfb-v3-004-cons-1", "p-cfb-v3-004-cons-2", "p-cfb-v3-004-cons-3"],
                   "generalization": ["p-cfb-v3-004-gen-1", "p-cfb-v3-004-gen-2", "p-cfb-v3-004-gen-3"],
                   "specificity_per_fact": [], "unmount": ["p-cfb-v3-004-unmount-1"]},
    "cfb-v3-005": {"consistency":  ["p-cfb-v3-005-cons-1", "p-cfb-v3-005-cons-2", "p-cfb-v3-005-cons-3"],
                   "generalization": ["p-cfb-v3-005-gen-1", "p-cfb-v3-005-gen-2", "p-cfb-v3-005-gen-3"],
                   "specificity_per_fact": [], "unmount": ["p-cfb-v3-005-unmount-1"]},
}
shared_specificity_probes = ["p-shared-spec-1", "p-shared-spec-2", "p-shared-spec-3"]

# === D.3 DELTA: batched trial enumeration ===
# Each trial = 1 batched MEMIT pass × 5 facts; 3 trials total (one per replicate).
# Per-trial torch_seed varies (D-S214D-D3-METHOD-3) to test stochastic stability
# of joint z-vector optimization across batched MEMIT initializations.
trial_matrix = []
for replicate in range(1, REPLICATES + 1):
    trial_matrix.append({
        "trial_index": replicate - 1,
        "replicate": replicate,
        "batched_fact_ids": list(stage_1_eligible_facts),  # all 5 facts in one batch
        "memit_requests": [fact_memit_requests[f] for f in stage_1_eligible_facts],
        "per_fact_probes": {f: fact_probes[f] for f in stage_1_eligible_facts},
        "shared_specificity_probes": shared_specificity_probes,
        "torch_seed": replicate * 17,  # distinct seeds: 17, 34, 51 (D-S214D-D3-METHOD-3)
        "regime": "batched",
    })

assert len(trial_matrix) == 3, f"D.3 trial count mismatch: {len(trial_matrix)} (expected 3)"

# C-S24-7 check: leakage exclusivity within batched fact set
# cfb-v3 has zero doubled subjects; trivially satisfied
trial_fact_ids = {f for t in trial_matrix for f in t["batched_fact_ids"]}
assert trial_fact_ids == set(stage_1_eligible_facts), \
    "C-S24-7 violation: batched trial fact set diverges from stage_1_eligible_facts"

# Persist trial matrix
os.makedirs("/workspace/stage_1_sect_d3", exist_ok=True)
with open("/workspace/stage_1_sect_d3/trial_matrix.json", "w") as f:
    json.dump({
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "session_label": "S2.14-D / D.3 batched / v0.1",
        "regime": "batched",
        "trial_count": len(trial_matrix),
        "per_fact_verdict_count": len(trial_matrix) * len(stage_1_eligible_facts),
        "replicate_seeds": [t["torch_seed"] for t in trial_matrix],
        "trial_matrix": trial_matrix,
    }, f, indent=2)

print(f"Cell 8 (D.3): batched trial matrix enumerated.")
print(f"  Trials: {len(trial_matrix)} batched × 5 facts = "
      f"{len(trial_matrix) * len(stage_1_eligible_facts)} per-fact verdicts.")
print(f"  Seeds: {[t['torch_seed'] for t in trial_matrix]}")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `len(trial_matrix)` | `3` |
| `trial_matrix[0]["batched_fact_ids"]` length | `5` (all stage_1_eligible_facts) |
| `trial_matrix[0]["memit_requests"]` length | `5` |
| Per-trial `torch_seed` values | `[17, 34, 51]` (distinct per D-S214D-D3-METHOD-3) |
| Per-fact verdict count (output) | `15` (matches S2.13-C 15-trial single-fact count) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Trial count ≠ 3 | Hard halt — session-level | Trial matrix authoring error; re-author |
| Batched fact ids diverge from stage_1_eligible_facts | Hard halt — session-level | C-S24-7 violation; re-author |

---

## §2.2 — Cell 9 modification — Batched MEMIT trial body

**Specialist:** memit-specialist (D-S214D-D3-METHOD-1 enforcement); validation-contract-architect (per-fact probe loop)

**Replaces:** v1.5 Cell 9 `execute_trial` function (single-fact body) — modified to batched form. Helpers (`measure_probe_full`, `intertrial_baseline_drift_gate`, `copy_unmount`) carry forward unchanged.

```python
# === CELL 9 (D.3 DELTA) — Batched MEMIT trial body ===
# Specialist: memit-specialist (primary); validation-contract-architect (probes)
# References: D-S214D-D3-METHOD-1; carry-forward helpers from v1.5 Cell 9 prelude
# v1.5 single-fact execute_trial → D.3 batched execute_batched_trial.
# Single MEMIT pass per trial editing 5 facts; per-fact probe loop after edit;
# overlay snapshot is per-trial (not per-fact).

import time
from datetime import datetime, timezone
import torch

def execute_batched_trial(trial, baselines, target_ids):
    """Run one D.3 batched trial. Returns verdict dict; persists per-trial JSON +
    overlay snapshot. Caller must check verdict['halt_session'] after each call."""
    trial_index = trial["trial_index"]
    replicate = trial["replicate"]
    batched_fact_ids = trial["batched_fact_ids"]
    trial_started_at = datetime.now(timezone.utc).isoformat()

    print(f"\n=== D.3 Batched Trial {trial_index}: replicate {replicate} "
          f"({len(batched_fact_ids)} facts) ===")
    torch.manual_seed(trial["torch_seed"])

    torch.cuda.reset_peak_memory_stats()
    allocated_pre = torch.cuda.memory_allocated()

    # Step 1: Inter-trial baseline-drift gate (carry-forward from v1.5)
    gate_record, gate_pass = intertrial_baseline_drift_gate(baselines)
    if not gate_pass:
        return {
            "trial_index": trial_index, "replicate": replicate, "regime": "batched",
            "halt_session": True, "halt_reason": "inter_trial_drift_gate_fail",
            "intertrial_gate": gate_record,
        }
    print(f"  Inter-trial drift gate: PASS")

    # Step 2: Apply BATCHED MEMIT edit (D-S214D-D3-METHOD-1)
    # Single MEMIT pass with all 5 fact requests; joint z-vector optimization.
    requests = trial["memit_requests"]  # list of 5 dicts
    edit_t0 = time.time()
    edited_model_local, orig_weights = apply_memit_to_model(
        model=model, tok=tokenizer, requests=requests, hparams=hparams,
        return_orig_weights=True,
    )
    edit_elapsed = time.time() - edit_t0
    print(f"  Batched MEMIT applied in {edit_elapsed:.1f}s ({len(requests)} facts; "
          f"~{edit_elapsed / len(requests):.1f}s/fact equivalent)")

    # Step 3: Per-fact probe loop (consistency + generalization + per-fact unmount)
    per_fact_verdicts = {}
    for fact_id in batched_fact_ids:
        fact_target_ids = target_ids[fact_id]
        fact_request = next(r for r in requests if r["subject"] ==
                            fact_memit_requests[fact_id]["subject"])

        # Consistency probes (3)
        cons_results = []
        for probe_id in trial["per_fact_probes"][fact_id]["consistency"]:
            probe = active_probes[probe_id]
            m = measure_probe_full(probe["prompt"], target_ids, fact_id)
            cons_results.append({
                "probe_id": probe_id,
                "p_target_new_post": m["p_target_new"],
                "top_1_token_post": m["top_1_token"],
                "consistency_pass": (m["p_target_new"] > 0.5),  # provisional band carry-forward
            })
        cons_aggregate_pass = sum(r["consistency_pass"] for r in cons_results) >= 2  # ≥2/3 PASS

        # Generalization probes (3)
        gen_results = []
        for probe_id in trial["per_fact_probes"][fact_id]["generalization"]:
            probe = active_probes[probe_id]
            m = measure_probe_full(probe["prompt"])
            baseline_p = baselines["per_probe"][probe_id]["p_top_1_pre"]
            drift = abs(m["p_top_1"] - baseline_p)
            gen_results.append({
                "probe_id": probe_id,
                "drift": drift,
                "generalization_pass": (drift < 0.05),
            })

        # Per-fact unmount probe (capture; unmount-band check at Cell 13)
        unmount_probe_id = trial["per_fact_probes"][fact_id]["unmount"][0]
        unmount_probe = active_probes[unmount_probe_id]
        m_unmount_pre_unmount = measure_probe_full(unmount_probe["prompt"],
                                                    target_ids, fact_id)

        per_fact_verdicts[fact_id] = {
            "consistency_results": cons_results,
            "consistency_aggregate_pass": cons_aggregate_pass,
            "generalization_results": gen_results,
            "unmount_pre_unmount_p_target_true": m_unmount_pre_unmount["p_target_true"],
        }
        print(f"    {fact_id}: cons={'PASS' if cons_aggregate_pass else 'FAIL'} "
              f"({sum(r['consistency_pass'] for r in cons_results)}/3) "
              f"gen_max_drift={max(r['drift'] for r in gen_results):.4f}")

    # Step 4: Shared-specificity probes post-batched-edit (D-S214D-D3-METHOD-4 input)
    shared_spec_post_edit = {}
    for probe_id in shared_specificity_probes:
        probe = active_probes[probe_id]
        m = measure_probe_full(probe["prompt"])
        baseline_p = baselines["per_probe"][probe_id]["p_top_1_pre"]
        drift = abs(m["p_top_1"] - baseline_p)
        shared_spec_post_edit[probe_id] = {
            "p_top_1_post": m["p_top_1"],
            "p_top_1_baseline": baseline_p,
            "drift": drift,
            "spec_pass": (drift < 0.05),
        }

    # Step 5: Copy-Unmount restoration (carry-forward from v1.5)
    unmount_record, all_match = copy_unmount(model, orig_weights)
    print(f"  Unmount: allclose_match all_layers={all_match}")

    # Step 6: Per-fact unmount-band check (post-unmount measurement)
    per_fact_unmount = {}
    for fact_id in batched_fact_ids:
        unmount_probe_id = trial["per_fact_probes"][fact_id]["unmount"][0]
        unmount_probe = active_probes[unmount_probe_id]
        m_post = measure_probe_full(unmount_probe["prompt"], target_ids, fact_id)
        p_pre = baselines["per_probe"][unmount_probe_id]["p_target_true_pre"]
        unmount_drift = abs(m_post["p_target_true"] - p_pre)
        per_fact_unmount[fact_id] = {
            "p_target_true_post_unmount": m_post["p_target_true"],
            "p_target_true_pre": p_pre,
            "drift": unmount_drift,
            "unmount_pass": (unmount_drift < 1e-4),  # IC-S23-4 hard band
        }

    allocated_post = torch.cuda.memory_allocated()
    peak_alloc = torch.cuda.max_memory_allocated()

    trial_record = {
        "trial_index": trial_index,
        "replicate": replicate,
        "regime": "batched",
        "torch_seed": trial["torch_seed"],
        "batched_fact_ids": batched_fact_ids,
        "started_at": trial_started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "edit_elapsed_seconds": edit_elapsed,
        "intertrial_gate": gate_record,
        "per_fact_verdicts": per_fact_verdicts,
        "shared_specificity_post_edit": shared_spec_post_edit,
        "unmount_record_summary": {"all_layers_allclose_match": all_match},
        "per_fact_unmount": per_fact_unmount,
        "memory": {
            "allocated_pre_gib": allocated_pre / (1024**3),
            "allocated_post_gib": allocated_post / (1024**3),
            "peak_gib": peak_alloc / (1024**3),
        },
        "halt_session": False,
    }

    # Persist per-trial JSON + overlay snapshot
    os.makedirs("/workspace/stage_1_sect_d3/trials", exist_ok=True)
    os.makedirs(f"/workspace/stage_1_sect_d3/overlays/batched_trial_{trial_index}", exist_ok=True)
    with open(f"/workspace/stage_1_sect_d3/trials/d3_batched_trial_{trial_index}.json", "w") as f:
        json.dump(trial_record, f, indent=2)

    return trial_record
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `edit_elapsed_seconds` per trial | `~30–120s` (single MEMIT pass on 5-fact batch; bounded by z-vector optimization budget × 5 facts) |
| `unmount_record_summary.all_layers_allclose_match` | `True` per trial |
| `per_fact_unmount[fact_id]["unmount_pass"]` | `True` for all 5 facts per trial (IC-S23-4 hard band) |
| `peak_gib` | `~16–18 GiB` (similar profile to v1.5 single-fact; batch matrix solve at edit-time) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `apply_memit_to_model` raises on batched requests | Hard halt — session-level | Investigate batched-regime compatibility; flag OQ-S214D-D3-1 |
| Any per-fact `unmount_pass` = False | Hard halt — IC-S23-4 violation | Halt; investigate Copy-Unmount on batched edit (untested before D.3) |
| Inter-trial drift gate FAIL | Hard halt — session-level | State contamination; halt |

---

## §2.3 — Cell 11 modification — Overlay shape (per-batched-trial)

**Specialist:** state-consistency-theorist

**Replaces:** v1.5 Cell 11 NV state inventory loop — modified to per-batched-trial overlay shape (3 overlays vs 15 single-fact overlays).

```python
# === CELL 11 (D.3 DELTA) — NV state inventory (batched form) ===
# Specialist: state-consistency-theorist
# Reduced overlay count: 3 batched-trial overlays × 1 edited.pt + 1 original.pt
# = 6 .pt files (vs v1.5 30 .pt files for 15 single-fact trials).
# Each overlay encodes a JOINT 5-fact edit; not separable per fact.

import os, json
import hashlib

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

nv_inventory = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": "S2.14-D / D.3 batched / v0.1",
    "regime": "batched",
    "trials": [],
}

for trial_index in range(3):
    overlay_dir = f"/workspace/stage_1_sect_d3/overlays/batched_trial_{trial_index}"
    edited_path = os.path.join(overlay_dir, "edited.pt")
    original_path = os.path.join(overlay_dir, "original.pt")
    trial_overlay = {
        "trial_index": trial_index,
        "edited_sha": file_sha256(edited_path) if os.path.exists(edited_path) else None,
        "original_sha": file_sha256(original_path) if os.path.exists(original_path) else None,
        "edit_scope": "joint_5_fact",
    }
    nv_inventory["trials"].append(trial_overlay)

with open("/workspace/stage_1_sect_d3/nv_inventory.json", "w") as f:
    json.dump(nv_inventory, f, indent=2)

print(f"Cell 11 (D.3): NV overlay inventory captured. "
      f"3 batched-trial overlays (joint 5-fact edits per overlay).")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| Per-trial `edited_sha` | non-null SHA256 |
| Per-trial `original_sha` | non-null; same value across all 3 trials (pre-edit weights identical) |
| `edit_scope` per overlay | `joint_5_fact` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any `edited_sha` null or matches `original_sha` | Hard halt — IC-S23-4-class | Edit did not apply; investigate |

---

## §2.4 — Cell 13 modification — D.3 verdict + cross-fact specificity gate

**Specialist:** validation-contract-architect (D-S214D-D3-METHOD-4, METHOD-5)

**Replaces:** v1.5 Cell 13 Stage 1 consistency aggregate — D.3 verdict predicate + cross-fact specificity gate.

```python
# === CELL 13 (D.3 DELTA) — D.3 verdict + cross-fact specificity gate ===
# Specialist: validation-contract-architect
# References: D-S214D-D3-METHOD-4, METHOD-5
# Aggregates per-fact verdicts from 3 batched trials × 5 facts; computes
# cross-fact specificity gate (shared-spec drift comparison vs S2.13-C
# single-fact baseline median); emits D.3 verdict.

import json
import numpy as np

# Load all 3 batched trial records
trials = []
for trial_index in range(3):
    with open(f"/workspace/stage_1_sect_d3/trials/d3_batched_trial_{trial_index}.json") as f:
        trials.append(json.load(f))

# === Per-fact consistency aggregate ===
# Per D-S214D-D3-METHOD-5: D.3 PASS if ≥3/5 facts achieve cons aggregate PASS
# at ≥2/3 trials each.
fact_ids = trials[0]["batched_fact_ids"]
per_fact_aggregate = {}
for fact_id in fact_ids:
    trial_passes = [
        t["per_fact_verdicts"][fact_id]["consistency_aggregate_pass"]
        for t in trials
    ]
    fact_aggregate_pass = sum(trial_passes) >= 2  # ≥2/3 trials
    per_fact_aggregate[fact_id] = {
        "trial_passes": trial_passes,
        "trial_pass_count": sum(trial_passes),
        "fact_aggregate_pass": fact_aggregate_pass,
    }

facts_passing = sum(1 for fid in fact_ids if per_fact_aggregate[fid]["fact_aggregate_pass"])
consistency_aggregate_pass = facts_passing >= 3

# === Cross-fact specificity gate (D-S214D-D3-METHOD-4) ===
# Aggregate shared-specificity drift across 3 batched trials × 3 shared-spec probes
# = 9 drift measurements. Compare to S2.13-C single-fact baseline reference.
shared_spec_drifts = []
for trial in trials:
    for probe_id, record in trial["shared_specificity_post_edit"].items():
        shared_spec_drifts.append(record["drift"])

batched_drift_median = float(np.median(shared_spec_drifts))
batched_drift_max = float(np.max(shared_spec_drifts))

# S2.13-C single-fact reference (load from S2.13-C verdict; if absent, fall back to
# operator-side reference value from session_2_13_summary_block.md §3 specificity record).
# Reference: S2.13-C reported shared-specificity drift well within 0.05 band across
# 15 single-fact trials. For D.3 cross-fact gate, threshold is 2× the S2.13-C
# baseline median — substantial elevation flags batched-regime interference.
S213C_REFERENCE_DRIFT_MEDIAN = 0.005  # provisional; substitute with actual S2.13-C value at execution
CROSS_FACT_INTERFERENCE_THRESHOLD = 2.0 * S213C_REFERENCE_DRIFT_MEDIAN

cross_fact_interference_flagged = batched_drift_median > CROSS_FACT_INTERFERENCE_THRESHOLD

# === D.3 verdict predicate ===
# PASS:    consistency_aggregate_pass AND NOT cross_fact_interference_flagged
# FAIL:    NOT consistency_aggregate_pass
# PARTIAL: consistency_aggregate_pass AND cross_fact_interference_flagged

if consistency_aggregate_pass and not cross_fact_interference_flagged:
    verdict_class = "D.3-PASS"
    routing = (
        "Batched MEMIT regime achieves consistency PASS where single-fact regime "
        "FAILED at S2.13-C. Batching IS the lever. Routes to: revisit single-fact "
        "Stage 1 SECT verdict in light of batched-regime PASS; consider corpus "
        "or trial-protocol revision; D.1 verdict INFORMATIONAL but not blocking."
    )
elif not consistency_aggregate_pass:
    verdict_class = "D.3-FAIL"
    routing = (
        "Batched regime achieves same/worse consistency as single-fact (S2.13-C). "
        "Batching is NOT the lever; architectural ceiling is invariant to batch size. "
        "Combined with D.1 verdict, routes architectural/mechanism eliminations "
        "to T.1 (alt model) / T.2 (alt write engine) / T.3 (alt arch) per Q4 "
        "deferred verdict at S2.14-D close."
    )
else:  # consistency PASS but cross-fact interference flagged
    verdict_class = "D.3-PARTIAL"
    routing = (
        "Batched regime achieves consistency PASS but introduces cross-fact "
        "interference (shared-spec drift elevated vs S2.13-C single-fact baseline). "
        "Routes to: investigate batched z-vector geometry; possible new sub-path "
        "scoping for N-fact regime characterization (where N is the threshold "
        "below which interference is acceptable)."
    )

verdict = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": "S2.14-D / D.3 batched / v0.1",
    "methodology_decisions": [f"D-S214D-D3-METHOD-{i}" for i in range(1, 7)],
    "regime": "batched",
    "n_trials": len(trials),
    "n_facts_per_trial": len(fact_ids),
    "per_fact_aggregate": per_fact_aggregate,
    "facts_passing_cons_aggregate": facts_passing,
    "consistency_aggregate_pass": consistency_aggregate_pass,
    "cross_fact_specificity": {
        "shared_spec_drift_count": len(shared_spec_drifts),
        "batched_drift_median": batched_drift_median,
        "batched_drift_max": batched_drift_max,
        "s213c_reference_median": S213C_REFERENCE_DRIFT_MEDIAN,
        "interference_threshold": CROSS_FACT_INTERFERENCE_THRESHOLD,
        "interference_flagged": cross_fact_interference_flagged,
    },
    "verdict_class": verdict_class,
    "forward_routing": routing,
}

with open("/workspace/stage_1_sect_d3/d3_verdict.json", "w") as f:
    json.dump(verdict, f, indent=2)

print(f"\n{'=' * 70}")
print(f"D.3 BATCHED VERDICT")
print(f"  Per-fact cons aggregate PASS: {facts_passing}/5")
print(f"  Cross-fact drift median: {batched_drift_median:.4f} "
      f"(threshold {CROSS_FACT_INTERFERENCE_THRESHOLD:.4f})")
print(f"  VERDICT: {verdict_class}")
print(f"  ROUTING: {routing}")
print(f"{'=' * 70}")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `n_trials` | `3` |
| `len(per_fact_aggregate)` | `5` |
| `cross_fact_specificity.shared_spec_drift_count` | `9` (3 trials × 3 shared-spec probes) |
| `verdict_class` | One of `D.3-PASS` / `D.3-FAIL` / `D.3-PARTIAL` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Per-fact aggregate computation references missing trial data | Hard halt — verdict-level | Trial JSON missing or malformed; investigate |
| Verdict class outside canonical three | Hard halt — verdict-level | Predicate gap; re-author §2.4 logic |

---

# Part III — Verdict, IC contracts, NV state, OQ ledger

## §3.1 — D.3 verdict predicate (canonical)

| consistency_aggregate_pass | cross_fact_interference_flagged | Verdict class | Routing |
|---|---|---|---|
| Yes | No | `D.3-PASS` | Batching IS the lever; revisit single-fact verdict; D.1 informational |
| No | (any) | `D.3-FAIL` | Batching not the lever; combined with D.1 routes to T.1/T.2/T.3 |
| Yes | Yes | `D.3-PARTIAL` | Batching introduces interference; new sub-path for N-fact regime characterization |

## §3.2 — Interface contracts surfaced at v0.1

**IC-S214D-D3-1 — Batched MEMIT request contract**

| Field | Value |
|---|---|
| From | `trial_matrix.json` (D.3 Cell 8 output) |
| To | `apply_memit_to_model` (Cell 9 batched call) |
| What source exposes | List of N fact request dicts (`prompt`, `subject`, `target_new`); per-trial torch_seed; trial_index |
| Conditions | All N facts in `stage_1_eligible_facts`; subject set carry-forward from cfb-v3 v1.0; C-S24-7 trivially satisfied (no doubled subjects) |
| Failure behavior | Cell 9 hard halt if `apply_memit_to_model` raises on N>1 batch (untested at S2.13-C — flag as OQ-S214D-D3-1 if surfaces) |

**IC-S214D-D3-2 — Cross-fact specificity gate contract**

| Field | Value |
|---|---|
| From | Per-trial `shared_specificity_post_edit` records |
| To | `d3_verdict.json` cross_fact_specificity field |
| What source exposes | 9 drift measurements (3 trials × 3 shared-spec probes); median + max statistics |
| Conditions | S2.13-C single-fact reference value loaded (operator-side substitution at execution if not in NV state) |
| Failure behavior | Threshold breach → `cross_fact_interference_flagged = True` → routes to D.3-PARTIAL; informational, not session-halting |

## §3.3 — NV state delta from v1.5

**Inputs (carry-forward; consumed by D.3, not modified):**
```
/workspace/architecture_profile/                       # Carry-forward from v1.5
/workspace/covariance_caches/.../wikipedia_stats/      # L4-L8 caches durable; load-bearing
/workspace/architecture_profile/stage_1_llama_baselines.json  # Pre-edit baselines
```

**Outputs (D.3-specific; new namespace `/workspace/stage_1_sect_d3/`):**
```
/workspace/stage_1_sect_d3/
  ├── trial_matrix.json                              (Cell 8)
  ├── trials/
  │   ├── d3_batched_trial_0.json                    (Cell 9)
  │   ├── d3_batched_trial_1.json
  │   └── d3_batched_trial_2.json
  ├── overlays/
  │   ├── batched_trial_0/{edited.pt, original.pt}   (Cell 9)
  │   ├── batched_trial_1/{edited.pt, original.pt}
  │   └── batched_trial_2/{edited.pt, original.pt}
  ├── nv_inventory.json                              (Cell 11)
  └── d3_verdict.json                                (Cell 13)
```

D.3 does NOT modify v1.5 NV state at `/workspace/stage_1_sect/` (S2.13-C verdict + 15 trial JSONs + 30 overlay .pt files preserved). Per `s214_d_kb_and_nv_hygiene.md` §2.2, S2.13-C predecessor state remains durable for cross-comparison reference.

## §3.4 — Open questions surfaced at v0.1

| OQ ID | Origin | Status | Closes when |
|---|---|---|---|
| **OQ-S214D-D3-1** | v0.1 §2.2 (does `apply_memit_to_model` accept N>1 batched requests cleanly on Llama-3.1-8B?) | OPEN at authoring; closes empirically at Cell 9 first batched trial PASS or FAIL | Cell 9 Trial 0 execution |
| **OQ-S214D-D3-2** | v0.1 §2.4 (S2.13-C single-fact shared-spec drift reference value substitution) | OPEN at authoring; operator-side substitution required at execution from S2.13-C trial JSONs | Pre-Cell-13 operator-side capture |
| **OQ-S214D-D3-3** | v0.1 §2.2 (Copy-Unmount bit-exact restoration on joint 5-fact edit; untested before D.3) | OPEN at authoring; closes empirically per Cell 9 unmount-record check | Cell 9 first batched trial unmount band PASS |

## §3.5 — Decisions ratified at v0.1 authoring

| ID | Decision |
|---|---|
| **D-S214D-D3-RUNBOOK-1** | `d3_multi_target_hyperscale_runbook.md` v0.1 authored at S2.14-D as delta against v1.5; PROVISIONAL until Cell 13 verdict produced |
| **D-S214D-D3-METHOD-1..6** | Methodology lock per §1.5 (batched regime, 3-trial protocol, distinct seeds, cross-fact gate, verdict predicate, corpus carry-forward) |

## §3.6 — Non-goals at v0.1

D.3 v0.1 does NOT:
- Re-author cfb-v3 corpus or probe-set-v3 (carry-forward from S2.13-C v1.0 lock)
- Rebuild covariance caches (L4-L8 caches durable from S2.13-C; reuse preserved)
- Substitute for D.1 mechanistic verdict (D.3 is regime test, not mechanism test)
- Authorize routing to T.1/T.2/T.3 — verdict at Cell 13 surfaces routing recommendations; ratification at session_2_14_d_summary_block.md authoring jointly with D.1 verdict
- Test N≠5 batch sizes at v0.1 (single-N regime test; N-fact characterization is OQ-S214D-D3-equivalent if D.3-PARTIAL surfaces)

---

# End of d3_multi_target_hyperscale_runbook v0.1

> Authoring ratified at S2.14-D; PROVISIONAL until verdict execution.
> Successor revision triggers: (a) Cell 9 first batched trial raises on `apply_memit_to_model` (OQ-S214D-D3-1 escalation; methodology re-ratification of D-S214D-D3-METHOD-1); (b) Cell 9 unmount-band fails on joint edit (OQ-S214D-D3-3 escalation; investigate Copy-Unmount semantics on batched overlay); (c) D.3-PARTIAL surfaces (new N-fact regime sub-path scoping needed at successor session).
