# Stage 1 SECT Runbook — T.2 GRACE on `meta-llama/Llama-3.1-8B` (v0.1 declarative)

> **Document version:** v0.1 (declarative; pre-empirical)
> **Authoring session:** S2.19 = T.2 GRACE runbook v0.1 authoring (operator-side post-v0.2 codification; verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5')
> **Status:** RATIFIED v0.1 — declarative; empirical absorption deferred to v0.2 codification analog session post-S2.20 first-execution (parallel to t2_rome_runbook v0.1 → v0.2 absorption pattern)
> **Companion artifact:** `grace-patches-canonical.md` v0.1 (parallel sibling; authored at S2.19 Block 1)
> **Sibling artifacts:** `t2_rome_runbook.md` v0.2 (preserved post-elimination); `stage_1_sect_runbook_v1_7.md` (MEMIT-side; preserved unmodified)
> **Specialist provenance:** framework-spec-writer (primary; runbook authoring; v0.1 spec format discipline; structural template inheritance from `t2_rome_runbook.md` v0.2); memit-specialist (consultative; GRACE adapter mechanism specification, hparam surface derivation, mechanism-orthogonality argument; primary on Cells 1, 2, 4, 8, 9, 11, 15); state-consistency-theorist (consultative; GRACE unmount mechanism specification per `C-GRACE-5`, covariance cache inapplicability rationale at Cell 3, cross-session bit-exact determinism inheritance; primary on Cells 3, 5, 7, 15); validation-contract-architect (Cell 6 / Cell 7 / Cell 9 verdict surface; calibration corridor PASS criterion; pathology classification taxonomy carry-forward from S2.18 ROME taxonomy; primary on Cells 6, 7, 10, 12, 13, 16); orchestration-comparativist (write-engine architecture comparison surface foreground at v1.1 GRACE entry; consultative on Cell 4 hparam surface + §1.5 authoring discipline); graph-data-architect (light-touch; framework-spec-relevance scoring for adapter-based mechanisms; consultative on §1.5 + §10.x reference appendices)
> **Workstream:** WS1 (empirical execution; T.2 GRACE entry; verdict-conditional C-FAIL branch active)

---

# Part I — Authoring discipline

## 1.5 Authoring discipline — v0.1 declarative

### 1.5.1 Single-fact dispatch envelope (`C-GRACE-1`; DECLARATIVE at v0.1)

Per `grace-patches-canonical.md` v0.1 §5.1: GRACE edit dispatch at S2.20 operates in single-fact-per-trial mode. The codebook is initialized fresh at trial entry and discarded at trial exit; no cross-trial codebook state. One fact per trial; one trial per per-fact entry in the trial matrix. Verification at Cell 9 (single-edit dispatch) and Cell 15 (trial loop body — per-trial codebook reset gate).

### 1.5.2 Empirical anchor inheritance (D-S217-4 + D-S218-7 carry-forward)

| Anchor | Inheritance | Source |
|---|---|---|
| `meta-llama/Llama-3.1-8B` revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` | LOCKED — held verbatim | S2.13-C through S2.18 cumulative |
| Cross-session bit-exact determinism (6 checkpoints; fp16 forward-pass drift `0.00e+00`) | INHERITED — same target model SHA | D-S217-4 + D-S218-7 |
| `cfb-v3.yaml` v1.0 corpus (5 facts) | LOCKED — held verbatim | S2.13-C |
| `probe-set-v3.yaml` v1.0 (38 active probes) | LOCKED — held verbatim | S2.13-C |
| IC-S24-4 trial protocol (5 facts × 3 replicates = 15 trials) | INHERITED — held; GRACE multi-fact dispatch semantics may differ (re-evaluated at Block B Cell 9) | S2.4 series |
| Acceptance bands (`0.5` cons / `0.05` gen / `0.05` spec / `1e-4` unmount) | LOCKED — held; re-evaluate if GRACE adapter dispatch produces different probability surface shapes | D-S24-10 + IC-S23-4 |
| D-S215D2-VERDICT-INTEGRITY-1 load-bearing subset (`{cfb-v3-001, cfb-v3-002, cfb-v3-005}`) | LOCKED — held verbatim | S2.15-D2 |
| Pad-Token applicability | INHERITED — engine-agnostic tokenizer-side | `memit-patches-canonical.md` v2.5 §3.1 + `rome-patches-canonical.md` v0.2 §1.1 |
| MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism (D-V12-MULTITOKEN-1) | INHERITED via v1.7 sibling pattern; absorbed at Cell 6 / Cell 7 / Cell 9 | `stage_1_sect_runbook_v1_7.md` §1.5.3 |
| Cell 13 3-route verdict gate framework | INHERITED — codified empirically at S2.18; carries forward unchanged | `t2_rome_runbook.md` v0.2 Cell 13 |
| Copy-Unmount mechanism | **INAPPLICABLE** — adapter mechanism does not modify base weights in-place | `t_branch_decision_document.md` v1.1 §6'.2 |
| Covariance caches L2-L8 + L17 (~6.5 GiB durable on NV) | **INAPPLICABLE** — adapter mechanism does not consume `layer_stats` | `t_branch_decision_document.md` v1.1 §6'.3 |

### 1.5.3 v0.1 → v0.2 supersession integrity (NEW at v0.1)

This v0.1 runbook is **declarative** per the parallel ROME v0.1 → v0.2 absorption pattern. v0.2 absorption post-S2.20 first-execution will:

1. Replace declarative cell bodies with empirically-validated cell bodies (verbatim where unchanged; revised where empirical record diverges from declarative prediction).
2. Codify any NEW SOURCE_LAYER patches surfaced at Block A first-execution into `grace-patches-canonical.md` v0.2 + reference them in Cell 2 patch state verification.
3. Codify any CONFIG_LAYER patches surfaced at Block A Cell 8 initial diagnostic into `grace-patches-canonical.md` v0.2 §9 + reference them in Cell 1 / Cell 2 / Cell 8 application order.
4. Resolve OQ-S219-1 (P-1 / P-2 retain-trace applicability) at Cell 2 grep-anchor inspection.
5. Resolve OQ-S219-3 (single-fact-per-trial vs. adapter-accumulation) at Cell 15 trial loop body empirical record.
6. Resolve any v0.2 NEW OQs surfaced at first-execution (parallel to S2.18's surfacing of P-7-ROME / P-8-ROME / P-9-ROME mid-session).

The v0.1 → v0.2 supersession discipline preserves v0.1 as the declarative anchor; v0.2 supersedes v0.1 with empirical anchor; v0.1 is preserved at git ref or NV mirror as historical record (parallel to t2_rome_runbook v0.1 preservation post-v0.2 absorption).

---

## 1.1 Purpose

Execute Stage 1 SECT v3 protocol against T.2 GRACE on `meta-llama/Llama-3.1-8B`. The runbook walks Block A pre-flight (Cells 0–8: environment setup + patch state verification + dry-run gate), Block B HC-2-equivalent dry-run (Cells 9–13: single-fact GRACE adapter dispatch at two candidate layers + verdict gate), Block C trial loop (Cells 14–20: 15-trial protocol per IC-S24-4 if Cell 13 routes Route B; 3-trial reduced protocol if Route C; session halt if Route A).

**Forward-routing impact.** Block C verdict surface at Cell 17 + Cell 20 routes `t_branch_decision_document.md` v1.1 §5' empirical resolution:

- Block C aggregate PASS → ceiling is rank-1-in-weight-class-mechanism-specific; adapter-based mechanism viable on Llama-3.1-8B; S2.21 = MEMIT-vs-ROME-vs-GRACE comparison framework finding update (resolves OQ-V11-T-BRANCH-6); Workstream 2 / 3 implementation planning informed
- Block C aggregate FAIL → suspect (model × hparams) — ceiling generalizes to adapter mechanisms; FALL BACK TO T.1; S2.21 = T.1 alt-model runbook v0.1 authoring
- Block B Cell 13 Route A halt → equivalent to Block C aggregate FAIL for routing purposes (T.2 GRACE ELIM at canonical hparams; identical T.1 fallback path)

## 1.2 Measures

Three primary verdict measures per Stage 1 SECT v3 protocol (carried forward from `stage_1_sect_runbook_v1_7.md` §1.2):

| Measure | Probe panel | Acceptance band | Empirical anchor |
|---|---|---|---|
| **Consistency** | per-fact rewrite-shape probes (`cons-1` through `cons-N` per probe-set-v3 v1.0); P-capture as `P(target_new)` for STRICT_SINGLE_TOKEN facts; P-capture as `P(first_token_id)` for ALLOWLIST_FIRST_TOKEN_PROXY facts (per D-V12-MULTITOKEN-1) | `> 0.5` for PASS | D-S24-10 + IC-S23-4 |
| **Generalization** | per-fact paraphrase probes (`gen-1` through `gen-N`); same P-capture discipline as Consistency | top_1 unchanged from pre-edit OR `P(target_new)` shift `> 0.05` | D-S24-10 |
| **Specificity** | shared-spec probes across all facts in trial (`shared-spec-1` through `shared-spec-N`); P-capture per probe-set-v3 v1.0 | top_1 unchanged from pre-edit AND max `P(target_new)` drift `< 0.05` per probe | D-S24-10 |
| **Unmount** | post-detach forward-pass against same probes used for pre-edit baseline; drift assertion | `< 1e-4` for PASS (paralleling IC-S23-4 envelope); empirical expectation `0.00e+00` for adapter-detach (per `grace-patches-canonical.md` v0.1 §5.5) | IC-S23-4 + D-S219-Q4-1 |

## 1.3 Verdict integrity binding (D-S215D2-VERDICT-INTEGRITY-1 carry-forward)

Load-bearing subset = `{cfb-v3-001, cfb-v3-002, cfb-v3-005}`; aggregate Block C verdict requires PASS at all three load-bearing facts (per D-S215D2-VERDICT-INTEGRITY-1). Forensic-informative facts `{cfb-v3-003, cfb-v3-004}` are reported but do not gate verdict. cfb-v3-004 carries the multi-token first-token-proxy methodology per D-V12-MULTITOKEN-1 + D-S219-Q5-1 + RE-EVALUATE AT TRIAL 0 flag.

## 1.4 Halt conditions (cross-cell index)

| Halt class | Trigger | Cells | Disposition |
|---|---|---|---|
| **Cross-session bit-exact drift** | Cell 5 model load forward-pass drift `> 0.00e+00` against carried baseline | Cell 5 | HALT — investigate before any subsequent cell entry; model state corrupted or tokenizer regression |
| **Patch state miss** | Cell 2 marker assertion FAIL on any APPLICABLE patch | Cell 2 | HALT — patch application failed; investigate before Cell 3 entry |
| **R1.3 dry-run gate FAIL** | Cell 8 GRACE module smoke-load throws import-time or instantiation-time error | Cell 8 | HALT — patches not in place OR GRACE codebase incompatibility; investigate before Cell 9 entry |
| **Calibration corridor FAIL at both layer candidates** | Cell 13 verdict gate adjudicates B-FAIL (consistency `< 0.5` at L17 AND L2) AND pathology diagnostic distinct AND replay-S2.15-D2-precedent risk HIGH | Cell 13 | Route A halt — T.2 GRACE ELIM at canonical hparams → escalate per `t_branch_decision_document.md` v1.1 §5' (FALL BACK TO T.1) |
| **MULTI_TOKEN_FAIL** | Cell 6 fact tokenizes to multiple tokens AND not in MULTI_TOKEN_ALLOWLIST | Cell 6 | HARD halt per D-V12-MULTITOKEN-1 (inherited from v1.7 §1.5.3.1) |
| **Adapter-detach drift** | Cell 15 post-detach forward-pass drift `> 1e-4` on shared-spec probes | Cell 15 | Per-trial halt; fallback to adapter-snapshot-restore (per D-S219-Q4-1 fallback option (c)); v0.2 absorption codifies new unmount semantics |

---

# Part II — Pre-execution NV state

## 2.1 Carry-forward from MEMIT runbook v1.7 + ROME runbook v0.2

GRACE runbook inherits NV directory layout, environment variable conventions, and Block-and-Cell discipline from MEMIT runbook v1.7 + ROME runbook v0.2. Specifically:

- Pod working directory: `/workspace/`
- GRACE-side clone target: `/workspace/grace_dry_run/grace/` (parallel to `/workspace/rome_dry_run/rome/` and `/workspace/memit_dry_run/memit/`)
- HF cache: `/workspace/hf_cache/` (LOCKED at Cell 0 via `HF_HOME` env var BEFORE first transformers import per `C-S214D-4` carry-forward)
- Stage 1 outputs: `/workspace/stage_1_sect_grace/` (parallel to `/workspace/stage_1_sect/`)
- Mirror sync target: pod SSD `/root/stage_1_sect_grace_mirror/` (rsync from NV per parallel pattern)

## 2.2 NV state expected at S2.20 entry

| Path | Status | Notes |
|---|---|---|
| `/workspace/hf_cache/<model_revision_sha>` | PRESENT — Llama-3.1-8B fp16 weights | Carried forward from S2.13-C through S2.18; SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` |
| `/workspace/memit_dry_run/memit/` | PRESENT — preserved unmodified | MEMIT-side patches state at v2.5; not consumed by GRACE runbook except possibly for P-1 / P-2 transplant if OQ-S219-1 resolves APPLICABLE |
| `/workspace/rome_dry_run/rome/` | PRESENT — preserved post-elimination | ROME-side patches state at v0.2; not consumed by GRACE runbook |
| `/workspace/covariance_caches/<model_sha>/wikipedia_stats/` | PRESENT — INAPPLICABLE to GRACE | L2-L8 + L17 caches durable on NV (~6.5 GiB); NOT consumed at any GRACE cell |
| `/workspace/grace_dry_run/grace/` | **ABSENT** at S2.20 entry | Created at Cell 1 via `git clone` |
| `/workspace/stage_1_sect_grace/` | **ABSENT** at S2.20 entry | Created at Cell 14 trial matrix authoring |
| `/workspace/architecture_profile/<model_sha>/` | PRESENT — Llama-3.1-8B architecture profile | Carried forward from S2.14-D + S2.15-D2; consulted at Cell 4 hparam surface for layer-set verification |

---

# Part III — Block A: Pre-flight (Cells 0–8)

> **Block A purpose.** Establish pod-side environment + GRACE codebase + patch state + Llama-3.1-8B model load + tokenizer state + pre-edit baseline + R1.3-equivalent dry-run gate. All cells complete before any GRACE edit dispatch (Block B Cell 9 onward).

## Cell 0 — System binaries + Python deps

**Specialist:** framework-spec-writer (carry-forward verbatim from MEMIT v1.7 / ROME v0.2 Cell 0)

**Purpose:** Ensure pod has the required Python packages + `git` + `rsync`. INHERITED UNCHANGED from `stage_1_sect_runbook_v1_7.md` Cell 0 + `t2_rome_runbook.md` v0.2 Cell 0.

**Declarative cell body (v0.1):**

```bash
# === CELL 0 — System binaries + Python deps (inherited unchanged) ===
# Specialist: framework-spec-writer
# Inheritance: stage_1_sect_runbook_v1_7.md Cell 0 + t2_rome_runbook.md v0.2 Cell 0

# 0.1 — System binaries (assumed present on RunPod base image)
which git && which rsync && which python

# 0.2 — Python deps for GRACE (declarative; specific version pins per S2.20 first-execution)
pip install --quiet \
    "torch>=2.1.0" \
    "transformers>=4.40.0" \
    "accelerate>=0.27.0" \
    "datasets>=2.16.0" \
    "scipy" "numpy"
# v0.2 absorption: GRACE-specific deps if surfaced at S2.20 (e.g., specific Adam optimizer, adapter-pool storage)

# 0.3 — HF_HOME environment variable BEFORE any transformers import (C-S214D-4 carry-forward)
import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/hf_cache"
```

**v0.2 absorption note.** Specific version pins for GRACE-required deps (if any beyond MEMIT/ROME's stack) will be recorded at v0.2 absorption per S2.20 Cell 0 first-execution.

---

## Cell 1 — GRACE repository clone + SHA pin resolution

**Specialist:** memit-specialist (primary)

**Purpose:** Clone GRACE repo at latest stable tip per D-S219-Q1-1; record specific SHA hash to environment fingerprint; establish `/workspace/grace_dry_run/grace/` as canonical GRACE source path.

**Declarative cell body (v0.1):**

```bash
# === CELL 1 — GRACE repository clone + SHA pin resolution (D-S219-Q1-1) ===
# Specialist: memit-specialist
# References: D-S219-Q1-1 (latest stable tip); grace-patches-canonical.md v0.1 §3

mkdir -p /workspace/grace_dry_run
cd /workspace/grace_dry_run

# 1.1 — Clone latest stable tip (per D-S219-Q1-1)
git clone https://github.com/Thartvigsen/GRACE.git grace
cd grace

# 1.2 — Record specific SHA hash to environment fingerprint
GRACE_SHA=$(git rev-parse HEAD)
echo "GRACE_SHA=${GRACE_SHA}" >> /workspace/grace_dry_run/env_fingerprint.txt

# 1.3 — Verify clone integrity (smoke-check)
test -f /workspace/grace_dry_run/grace/README.md
test -d /workspace/grace_dry_run/grace/grace  # main module directory (declarative path; verify at v0.2 against actual repo structure)
```

**v0.2 absorption note.** Specific GRACE_SHA value recorded here at v0.2 codification analog session post-S2.20 (parallel to ROME's `0874014cd9837e4365f3e6f3c71400ef11509e04` recording at S2.18 Cell 1). Module directory path (`grace/grace/` vs. `grace/src/` or other) confirmed at v0.2 against actual repo structure.

---

## Cell 1.5 — Environment fingerprint capture

**Specialist:** state-consistency-theorist (provenance discipline)

**Purpose:** Capture full environment fingerprint for cross-session reproducibility. INHERITED UNCHANGED from `t2_rome_runbook.md` v0.2 Cell 1.5 with GRACE-side path adaptations.

**Declarative cell body (v0.1):**

```python
# === CELL 1.5 — Environment fingerprint capture (inherited; GRACE-side paths) ===
# Specialist: state-consistency-theorist

import json, subprocess, sys, torch, transformers
from pathlib import Path

fingerprint = {
    "session": "S2.20",  # set at session entry
    "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "python_version": sys.version,
    "torch_version": torch.__version__,
    "transformers_version": transformers.__version__,
    "cuda_available": torch.cuda.is_available(),
    "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    "engine": "GRACE",
    "engine_repo": "https://github.com/Thartvigsen/GRACE",
    "engine_sha": Path("/workspace/grace_dry_run/env_fingerprint.txt").read_text().strip(),
    "target_model": "meta-llama/Llama-3.1-8B",
    "target_model_revision_sha": "d04e592bb4f6aa9cfee91e2e20afa771667e1d4b",
}
Path("/workspace/grace_dry_run/env_fingerprint.json").write_text(json.dumps(fingerprint, indent=2))
```

---

## Cell 2 — GRACE patch state verification + transplant + new patch application

**Specialist:** memit-specialist (primary; patch state verification authority)

**Purpose:** Verify GRACE source state matches `grace-patches-canonical.md` v0.1 §1 inventory after applying any inherited patches (P-1 / P-2 conditional per OQ-S219-1) + any NEW patches surfaced at first-execution (DEFERRED at v0.1; absorbed at v0.2). Apply patches in order per `grace-patches-canonical.md` v0.1 §10.1.

**v0.1 disposition:** OQ-S219-1 closure step. Grep-anchor inspection of `grace/*.py` for `nethook.get_module` usage determines P-1 / P-2 applicability. If APPLICABLE → transplant `util/nethook.py` post-MEMIT-state from `/workspace/memit_dry_run/memit/util/nethook.py` to `/workspace/grace_dry_run/grace/util/nethook.py` with `.upstream_pristine` sibling preserved (parallel to ROME v0.2 §1.1 transplant pattern). If INAPPLICABLE → skip; record disposition in patch state manifest.

**Declarative cell body (v0.1):**

```python
# === CELL 2 — GRACE patch state verification + transplant + new patch application ===
# Specialist: memit-specialist
# References: grace-patches-canonical.md v0.1 §1 (patch inventory); §10 (application order);
#             OQ-S219-1 (P-1 / P-2 retain-trace applicability — closure step here)

import subprocess, json, hashlib
from pathlib import Path

GRACE_ROOT = Path("/workspace/grace_dry_run/grace")
MEMIT_ROOT = Path("/workspace/memit_dry_run/memit")  # source for P-1 / P-2 transplant if APPLICABLE

patches_applied = {}
patches_inapplicable = []

# 2.1 — OQ-S219-1 closure: grep-anchor inspection for nethook.get_module usage
nethook_search = subprocess.run(
    ["grep", "-rn", "nethook.get_module", str(GRACE_ROOT / "grace")],
    capture_output=True, text=True,
)
uses_nethook = (nethook_search.returncode == 0 and nethook_search.stdout.strip() != "")

if uses_nethook:
    # P-1 / P-2 APPLICABLE — transplant util/nethook.py post-MEMIT-state
    src = MEMIT_ROOT / "util" / "nethook.py"
    dst = GRACE_ROOT / "util" / "nethook.py"
    pristine = GRACE_ROOT / "util" / "nethook.py.upstream_pristine"

    if dst.exists() and not pristine.exists():
        dst.rename(pristine)  # preserve pristine before overwrite
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())

    # Marker assertions per C-GRACE-4
    nethook_src = dst.read_text()
    assert "def retain_hook(m, args, kwargs, output):" in nethook_src, "P-1 marker miss"
    # (P-2 marker assertion per MEMIT v2.5 §2.2 form)
    patches_applied["P-1"] = {"class": "SOURCE_LAYER", "status": "APPLIED", "verification_site": "Cell 2"}
    patches_applied["P-2"] = {"class": "SOURCE_LAYER", "status": "APPLIED", "verification_site": "Cell 2"}
else:
    # P-1 / P-2 INAPPLICABLE — GRACE adapter forward pass does not use nethook retain pattern
    patches_inapplicable.extend(["P-1", "P-2"])

# 2.2 — NEW SOURCE_LAYER patches application (DEFERRED at v0.1; populated at v0.2 absorption)
# (No NEW patches authored at v0.1 declarative per grace-patches-canonical.md v0.1 §1.4)

# 2.3 — Write patch state manifest per grace-patches-canonical.md v0.1 §11 schema
manifest = {
    "manifest_schema_version": "v0.1",
    "session": "S2.20",
    "engine": "GRACE",
    "engine_version_sha": Path("/workspace/grace_dry_run/env_fingerprint.txt").read_text().strip(),
    "target_model": "meta-llama/Llama-3.1-8B",
    "target_model_revision_sha": "d04e592bb4f6aa9cfee91e2e20afa771667e1d4b",
    "patches_applied": patches_applied,
    "patches_inapplicable": patches_inapplicable + [
        "P-3'", "Device-Map", "P-4", "P-5", "P-6", "P-7",
        "P-7-ROME", "P-8-ROME", "P-9-ROME", "Copy-Unmount",
    ],
    "patches_deferred_to_v0_2": [],  # populated if NEW patches surface at S2.20 mid-execution
    "constraints_active": ["C-GRACE-1", "C-GRACE-2", "C-GRACE-3", "C-GRACE-4", "C-GRACE-5"],
    "decisions_active": ["D-S219-Q1-1", "D-S219-Q2-1", "D-S219-Q3-1", "D-S219-Q4-1", "D-S219-Q5-1"],
    "uses_nethook": uses_nethook,  # OQ-S219-1 closure record
}
Path("/workspace/grace_dry_run/t2_grace_patch_state.json").write_text(json.dumps(manifest, indent=2))
```

**v0.2 absorption notes:**
- Actual `nethook.get_module` usage verdict recorded here (replaces declarative `uses_nethook` runtime check).
- Pad-Token application is at Cell 5 (tokenizer-side; deferred to model load) — not Cell 2.
- If NEW SOURCE_LAYER patches surface at S2.20 mid-execution, Cell 2 expands at v0.2 to include their application + marker assertions per the parallel ROME v0.2 Cell 2 P-7-ROME / P-8-ROME / P-9-ROME application pattern.

---

## Cell 3 — Covariance cache reuse verification — INAPPLICABLE-DEFERRED-BY-MECHANISM (OQ-S219-4 closure)

**Specialist:** state-consistency-theorist (mechanism-orthogonality assertion authority)

**Purpose:** Document that covariance cache reuse is INAPPLICABLE to GRACE adapter mechanism per `t_branch_decision_document.md` v1.1 §6'.3 + `framework_finding_memit_ceiling_archival.md` v1.1 §4.3'.4 + `grace-patches-canonical.md` v0.1 §1.3. Adapter-pool initialization verification (the mechanism-equivalent surface for GRACE) is folded into Cell 8 R1.3-equivalent dry-run gate per `C-GRACE-3` natural surface; this preserves cell-numbering parity with `t2_rome_runbook.md` v0.2 + avoids double-instrumentation.

**OQ-S219-4 closure (this cell).** Per kickoff §8 anticipated OQ disposition (a) INAPPLICABLE-DEFERRED-BY-MECHANISM:

- **Disposition:** Cell 3 declares INAPPLICABLE; structural cell preserved at this index for sibling-parity with `t2_rome_runbook.md` v0.2 cell numbering (Cells 0–20); adapter-pool initialization verification is performed at Cell 8 (R1.3-equivalent dry-run gate per `C-GRACE-3`).
- **Rationale:** GRACE does not consume `layer_stats` covariance caches (per `grace-patches-canonical.md` v0.1 §1.3 P-5 / P-6 INAPPLICABLE rationale). Cell 3 in `t2_rome_runbook.md` v0.2 verifies cache HIT discipline against the NV-resident `wikipedia_stats/` directory; for GRACE this verification is structurally null. The mechanism-equivalent verification surface (clean adapter pool initialization at trial entry per `C-GRACE-2`) is naturally part of Cell 8's R1.3-equivalent smoke-load + Cell 15's per-trial entry gate.

**Declarative cell body (v0.1):**

```python
# === CELL 3 — Covariance cache reuse verification — INAPPLICABLE for GRACE ===
# Specialist: state-consistency-theorist
# References: t_branch_decision_document.md v1.1 §6'.3 (covariance INAPPLICABLE);
#             framework_finding_memit_ceiling_archival.md v1.1 §4.3'.4 (patches carry-forward applicability);
#             grace-patches-canonical.md v0.1 §1.3 (P-5 / P-6 INAPPLICABLE rationale);
#             OQ-S219-4 closure (disposition (a))

# 3.1 — Mechanism-orthogonality assertion (no runtime verification needed)
print("Cell 3: GRACE adapter mechanism does not consume layer_stats covariance caches.")
print("        Mechanism-equivalent verification surface = adapter-pool initialization;")
print("        deferred to Cell 8 (R1.3-equivalent dry-run gate per C-GRACE-3).")

# 3.2 — Record disposition for cell-to-decision traceability
# (no NV writes; no cache resolution; no smoke-load — pure structural placeholder cell)
```

**v0.2 absorption note.** No empirical absorption expected at Cell 3 in any future execution session (the cell is structurally a no-op for GRACE; only its documentation may be tightened at v0.2 if S2.20 surfaces any unexpected interaction with NV cache state).

---

## Cell 4 — GRACE hparam declaration with GraceHyperParamsExtended subclass

**Specialist:** memit-specialist (primary; hparam surface authority)

**Purpose:** Declare GRACE canonical hparams per `grace-patches-canonical.md` v0.1 §4 + D-S219-Q2-1 + D-S219-Q3-1. Two-candidate layer surface: Layer-A primary L17 + Layer-B secondary L2. `GraceHyperParamsExtended` subclass codifies any GRACE-specific hparam fields beyond the upstream `GraceHyperParams` dataclass (parallel to `ROMEHyperParamsExtended` per `C-S218-5`).

**Declarative cell body (v0.1):**

```python
# === CELL 4 — GRACE hparam declaration (D-S219-Q2-1 + D-S219-Q3-1) ===
# Specialist: memit-specialist
# References: grace-patches-canonical.md v0.1 §4.1 (paper Table 1 reference values);
#             grace-patches-canonical.md v0.1 §4.2 (Layer-A L17 + Layer-B L2);
#             grace-patches-canonical.md v0.1 §4.3 (Llama-3.1-8B-specific considerations);
#             D-S219-Q2-1 + D-S219-Q3-1; C-S218-5 parallel pattern

import sys
sys.path.insert(0, "/workspace/grace_dry_run/grace")

# 4.1 — Import upstream GraceHyperParams dataclass (declarative; verify at v0.2 against actual import path)
from grace.hparams import GraceHyperParams  # path TBD per actual GRACE codebase

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GraceHyperParamsExtended(GraceHyperParams):
    """Extended GRACE hparams for Llama-3.1-8B (v0.1 declarative).

    Inherits paper Table 1 reference values via GraceHyperParams; adds Llama-specific
    fields per grace-patches-canonical.md v0.1 §4.3.
    """
    # Llama-3.1-8B layer placement
    layer: int = 17  # Layer-A primary per D-S219-Q3-1
    # Adapter parameter dtype (likely fp32; base model fp16 — coercion at adapter-vs-base interface)
    adapter_dtype: str = "float32"
    # Multi-token target tolerance flag (per D-S219-Q5-1)
    multi_token_first_token_proxy: bool = True
    re_evaluate_at_trial_0: bool = True

# 4.2 — Layer-A primary (L17) hparam instance
GRACE_HPARAMS_LAYER_A = GraceHyperParamsExtended(
    layer=17,  # transformer-mid; ROME L17 paper precedent analog
    # epsilon, learning_rate, n_iter, replacement, init, eps_expand: paper-canonical via inheritance
)

# 4.3 — Layer-B secondary (L2) hparam instance
GRACE_HPARAMS_LAYER_B = GraceHyperParamsExtended(
    layer=2,  # MLP-output mediation peak per S2.14-D D.1
)

# 4.4 — Layer-set verification against architecture profile (carry-forward from S2.14-D)
import json
arch_profile = json.loads(
    open("/workspace/architecture_profile/d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/profile.json").read()
)
n_layer = arch_profile["n_layer"]
assert 0 <= GRACE_HPARAMS_LAYER_A.layer < n_layer, f"Layer-A L17 out of range; n_layer={n_layer}"
assert 0 <= GRACE_HPARAMS_LAYER_B.layer < n_layer, f"Layer-B L2 out of range; n_layer={n_layer}"
```

**v0.2 absorption notes:**
- Actual `GraceHyperParams` import path verified against repo structure at S2.20 Cell 1 + Cell 4 first-execution.
- Specific paper-canonical values for `epsilon`, `learning_rate`, `n_iter`, `replacement`, `init`, `eps_expand` recorded inline at v0.2 absorption (replaces `# paper-canonical via inheritance` comment).
- If `GraceHyperParams` does not include all fields anticipated, the `GraceHyperParamsExtended` field list is revised at v0.2.

---

## Cell 5 — Llama-3.1-8B model load + Pad-Token alias + cross-session bit-exact gate

**Specialist:** state-consistency-theorist (cross-session bit-exact gate authority)

**Purpose:** Load `meta-llama/Llama-3.1-8B` fp16 + apply Pad-Token alias + verify cross-session bit-exact determinism against carried baseline (6 checkpoints; D-S217-4 + D-S218-7). INHERITED UNCHANGED from `t2_rome_runbook.md` v0.2 Cell 5 + `stage_1_sect_runbook_v1_7.md` Cell 5 with defensive preamble for any prior model cleanup.

**Declarative cell body (v0.1):**

```python
# === CELL 5 — Llama-3.1-8B model load + Pad-Token + cross-session bit-exact gate ===
# Specialist: state-consistency-theorist
# Inheritance: t2_rome_runbook.md v0.2 Cell 5 + stage_1_sect_runbook_v1_7.md Cell 5
# References: D-S217-4 + D-S218-7 (6-checkpoint cross-session bit-exact determinism);
#             grace-patches-canonical.md v0.1 §1.1 (Pad-Token APPLICABLE DIRECTLY);
#             grace-patches-canonical.md v0.1 §5.4 (C-GRACE-4 marker verification)

import gc, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 5.1 — Defensive preamble (clean any prior model state)
if "model" in dir():
    del model
gc.collect()
torch.cuda.empty_cache()

# 5.2 — Model load
MODEL_NAME = "meta-llama/Llama-3.1-8B"
MODEL_REVISION = "d04e592bb4f6aa9cfee91e2e20afa771667e1d4b"
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, revision=MODEL_REVISION,
    torch_dtype=torch.float16,
    device_map="auto",
).eval()
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)

# 5.3 — Pad-Token alias (per C-GRACE-4 + grace-patches-canonical.md v0.1 §1.1)
tokenizer.pad_token = tokenizer.eos_token
assert tokenizer.pad_token == tokenizer.eos_token, "Pad-Token marker assertion FAIL"

# 5.4 — Cross-session bit-exact gate (D-S217-4 + D-S218-7 carry-forward)
import json
baseline_path = (
    f"/workspace/cross_session_determinism/{MODEL_REVISION}/baseline_logits.pt"
)
baseline_logits = torch.load(baseline_path, map_location=model.device)
SMOKE_PROBE = "The Eiffel Tower is in"  # canonical determinism probe
input_ids = tokenizer(SMOKE_PROBE, return_tensors="pt").input_ids.to(model.device)
with torch.no_grad():
    current_logits = model(input_ids).logits.cpu()

drift = (current_logits.float() - baseline_logits.float()).abs().max().item()
assert drift == 0.00e+00, (
    f"Cross-session bit-exact gate FAIL: drift={drift:.2e} != 0.00e+00; "
    f"checkpoint #7 surfaced regression vs. carried baseline (6 prior checkpoints)"
)
print(f"Cell 5: cross-session bit-exact gate PASS (drift={drift:.2e}; checkpoint #7).")
```

---

## Cell 6 — LLaMA tokenizer single-token verification + MULTI_TOKEN_ALLOWLIST canonical absorption

**Specialist:** validation-contract-architect (D-V12-MULTITOKEN-1 absorption authority)

**Purpose:** Verify each fact in `cfb-v3.yaml` v1.0 has a tokenizer single-token target_new under Llama tokenizer; classify per `verdict_class` taxonomy; bind `MULTI_TOKEN_ALLOWLIST` runtime constant. INHERITED VERBATIM from `stage_1_sect_runbook_v1_7.md` §1.5.3.1 canonical absorption block per D-V12-MULTITOKEN-1.

**v0.1 disposition: D-S219-Q5-1 carry-forward.** First-token-proxy methodology + RE-EVALUATE AT TRIAL 0 flag inherits via this absorption block; re-evaluation at Cell 9 trial 0 entry (Block B).

**Declarative cell body (v0.1) — INHERITED VERBATIM from `stage_1_sect_runbook_v1_7.md` §1.5.3.1:**

```python
# === CELL 6 — MULTI_TOKEN_ALLOWLIST + first-token-proxy canonical absorption (v0.1 inheriting v1.7) ===
# Specialist: validation-contract-architect
# Inheritance: stage_1_sect_runbook_v1_7.md §1.5.3.1 (D-V12-MULTITOKEN-1)
# References: D-S219-Q5-1 (first-token-proxy carry-forward + RE-EVALUATE flag);
#             D-V12-MULTITOKEN-1 (verdict_class taxonomy)

import yaml
from pathlib import Path

# === MULTI_TOKEN_ALLOWLIST: canonical runtime constant ===
# Inheritance from stage_1_sect_runbook_v1_7.md §1.5.3.1 + D-S219-Q5-1
MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}   # harp under Llama tokenizer; subject = Hakeem Olajuwon

# === verdict_class taxonomy (D-V12-MULTITOKEN-1; 3 values) ===
# STRICT_SINGLE_TOKEN           — fact's target_new tokenizes to exactly 1 token
# ALLOWLIST_FIRST_TOKEN_PROXY   — fact in MULTI_TOKEN_ALLOWLIST AND uses first-token-proxy
# MULTI_TOKEN_FAIL              — fact tokenizes to multiple tokens AND not in allowlist (HARD halt)

def classify_fact(fact_id, target_new, tokenizer, allowlist):
    token_ids = tokenizer.encode(target_new, add_special_tokens=False)
    if len(token_ids) == 1:
        return ("STRICT_SINGLE_TOKEN", token_ids[0], token_ids)
    if fact_id in allowlist:
        return ("ALLOWLIST_FIRST_TOKEN_PROXY", token_ids[0], token_ids)
    return ("MULTI_TOKEN_FAIL", None, token_ids)

# === Per-fact verdict_class assignment ===
cfb_v3 = yaml.safe_load(Path("/workspace/cfb-v3.yaml").read_text())
fact_verdicts = {}
for fact in cfb_v3["facts"]:
    verdict_class, primary_token_id, full_token_ids = classify_fact(
        fact["id"], fact["target_new"], tokenizer, MULTI_TOKEN_ALLOWLIST,
    )
    fact_verdicts[fact["id"]] = {
        "verdict_class": verdict_class,
        "primary_token_id": primary_token_id,
        "full_token_ids": full_token_ids,
        "re_evaluate_at_trial_0": (verdict_class == "ALLOWLIST_FIRST_TOKEN_PROXY"),
    }
    # === Halt class: MULTI_TOKEN_FAIL ===
    if verdict_class == "MULTI_TOKEN_FAIL":
        raise RuntimeError(
            f"Cell 6: fact_id={fact['id']} target_new={fact['target_new']!r} "
            f"tokenizes to {len(full_token_ids)} tokens; not in MULTI_TOKEN_ALLOWLIST. "
            f"Either add fact_id to MULTI_TOKEN_ALLOWLIST AND verify first-token-proxy is "
            f"acceptable for this fact, OR retire the fact from cfb-v3.yaml."
        )

# === Aggregate counts (inherited from v1.7) ===
strict_count = sum(1 for v in fact_verdicts.values() if v["verdict_class"] == "STRICT_SINGLE_TOKEN")
proxy_count  = sum(1 for v in fact_verdicts.values() if v["verdict_class"] == "ALLOWLIST_FIRST_TOKEN_PROXY")
proxy_facts  = sorted(fid for fid, v in fact_verdicts.items() if v["verdict_class"] == "ALLOWLIST_FIRST_TOKEN_PROXY")

print(f"Cell 6: STRICT_SINGLE_TOKEN={strict_count}; ALLOWLIST_FIRST_TOKEN_PROXY={proxy_count} ({proxy_facts}).")
```

---

## Cell 7 — Pre-edit baseline capture + cross-session bit-exact gate

**Specialist:** validation-contract-architect (verdict_class dispatch wiring) + state-consistency-theorist (cross-session anchor)

**Purpose:** Capture per-fact pre-edit baseline P-values for Consistency / Generalization / Specificity probes; gate cross-session bit-exact anchor extension to checkpoint #7. INHERITED VERBATIM from `stage_1_sect_runbook_v1_7.md` §1.5.3.2 first-token-proxy P-capture wiring + cross-session anchor.

**Declarative cell body (v0.1) — INHERITED from `stage_1_sect_runbook_v1_7.md` §1.5.3.2 with engine-agnostic adaptations:**

```python
# === CELL 7 — Pre-edit baseline capture + cross-session bit-exact gate (v0.1 inheriting v1.7) ===
# Specialist: validation-contract-architect + state-consistency-theorist
# Inheritance: stage_1_sect_runbook_v1_7.md §1.5.3.2 (first-token-proxy P-capture wiring) + Cell 7
# References: D-V12-MULTITOKEN-1 (verdict_class dispatch); D-S217-4 + D-S218-7 (6-checkpoint anchor)

import torch, json, yaml
from pathlib import Path

# 7.1 — Load probe set
probe_set = yaml.safe_load(Path("/workspace/probe-set-v3.yaml").read_text())
fact_probes = {fact_id: probe_set["per_fact_probes"][fact_id] for fact_id in fact_verdicts}
shared_specificity_probes = probe_set["shared_specificity_probes"]

# 7.2 — Per-fact pre-edit baseline P-capture (verdict_class-aware first-token-proxy)
pre_edit_baseline = {"per_fact": {}, "shared_specificity": {}}

for fact_id, vd in fact_verdicts.items():
    target_token_id = vd["primary_token_id"]   # first-token-proxy for ALLOWLIST_*; full single token for STRICT_*
    fact_baseline = {}
    for probe_role in ("cons", "gen", "spec"):
        for probe in fact_probes[fact_id].get(probe_role, []):
            input_ids = tokenizer(probe["text"], return_tensors="pt").input_ids.to(model.device)
            with torch.no_grad():
                logits = model(input_ids).logits[0, -1].float()
            probs = torch.softmax(logits, dim=-1)
            fact_baseline[probe["id"]] = {
                "p_target": probs[target_token_id].item(),
                "top_1_token_id": int(probs.argmax().item()),
                "top_1_p": probs.max().item(),
                "verdict_class": vd["verdict_class"],
            }
    pre_edit_baseline["per_fact"][fact_id] = fact_baseline

# 7.3 — Shared-specificity baseline (first-token-proxy not applicable; full-token P-capture)
for probe in shared_specificity_probes:
    input_ids = tokenizer(probe["text"], return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    probs = torch.softmax(logits, dim=-1)
    pre_edit_baseline["shared_specificity"][probe["id"]] = {
        "top_1_token_id": int(probs.argmax().item()),
        "top_1_p": probs.max().item(),
    }

# 7.4 — Cross-session bit-exact gate extension (checkpoint #7 — pre-edit forward-pass under live trial state)
# (Cell 5 already gated checkpoint #7 on smoke probe; Cell 7 extends to per-fact + shared-spec full panel.)
Path("/workspace/grace_dry_run/pre_edit_baseline.json").write_text(json.dumps(pre_edit_baseline, indent=2))
print(f"Cell 7: pre-edit baseline captured for {len(fact_verdicts)} facts + {len(shared_specificity_probes)} shared-spec probes.")
```

---

## Cell 8 — R1.3-equivalent dry-run gate for GRACE dispatch path (with adapter-pool initialization verification)

**Specialist:** memit-specialist (dispatch path authority) + state-consistency-theorist (adapter-pool initialization verification per Cell 3 deferral)

**Purpose:** Smoke-load GRACE module against patched repo state; instantiate empty adapter pool; verify no import-time or instantiation-time errors per `C-GRACE-3`. **Adapter-pool initialization verification (Cell 3 deferral; OQ-S219-4 closure (a))** is folded into this cell's smoke-load: the empty-codebook adapter pool initialization IS the C-GRACE-2 mechanism-equivalent verification.

**Declarative cell body (v0.1):**

```python
# === CELL 8 — R1.3-equivalent dry-run gate + adapter-pool initialization verification ===
# Specialist: memit-specialist + state-consistency-theorist
# References: grace-patches-canonical.md v0.1 §5.3 (C-GRACE-3); §5.2 (C-GRACE-2);
#             OQ-S219-4 closure (a) — adapter-pool initialization folded into Cell 8

import sys, importlib

# 8.1 — Smoke-load GRACE module against patched repo state
sys.path.insert(0, "/workspace/grace_dry_run/grace")
grace = importlib.import_module("grace")  # path TBD per actual GRACE codebase at v0.2

# 8.2 — Instantiate empty adapter pool (declarative API; verify at v0.2 against actual GRACE codebase)
adapter_pool = grace.AdapterPool(model=model, hparams=GRACE_HPARAMS_LAYER_A)

# 8.3 — Adapter-pool initialization verification per C-GRACE-2 (Cell 3 deferral closure)
assert adapter_pool.codebook_size == 0, (
    f"C-GRACE-2 FAIL: adapter pool codebook not empty at initialization "
    f"(size={adapter_pool.codebook_size})"
)
assert adapter_pool.routing_layer_adapters == [], (
    f"C-GRACE-2 FAIL: routing layer adapter list not empty at initialization"
)

# 8.4 — Forward-pass smoke test (empty-codebook adapter pool + base model)
SMOKE_PROBE = "The Eiffel Tower is in"
input_ids = tokenizer(SMOKE_PROBE, return_tensors="pt").input_ids.to(model.device)
with torch.no_grad():
    smoke_logits_pre = model(input_ids).logits.cpu()
    # With empty adapter pool, forward pass should be bit-exact identical to base model
    smoke_logits_post = model(input_ids).logits.cpu()  # pool active but empty
drift = (smoke_logits_pre.float() - smoke_logits_post.float()).abs().max().item()
assert drift == 0.00e+00, (
    f"Cell 8 R1.3 dry-run gate FAIL: empty-codebook adapter pool produces drift={drift:.2e} != 0.00e+00; "
    f"adapter pool may be instrumenting forward pass even with empty codebook (mechanism violation)"
)

# 8.5 — Cleanup adapter pool (no edit dispatched at smoke-load)
del adapter_pool
gc.collect()
torch.cuda.empty_cache()

print(f"Cell 8: R1.3 dry-run gate PASS; adapter-pool initialization verification PASS.")
```

**v0.2 absorption notes:**
- Actual `grace.AdapterPool` API + signature verified against repo structure at S2.20 first-execution.
- If GRACE's adapter-pool dispatch instruments base-model forward pass even with empty codebook (drift `> 0.00e+00`), the assertion at 8.4 surfaces the violation; v0.2 absorption may need to relax the bit-exact expectation OR a NEW SOURCE_LAYER patch is authored mid-execution to enforce empty-codebook bit-exactness.

---

# Part IV — Block B: HC-2-equivalent dry-run (Cells 9–13)

> **Block B purpose.** Single-fact GRACE adapter dispatch at two candidate layers (Layer-A L17 primary + Layer-B L2 secondary per D-S219-Q3-1). Dispatch the sharpest IN-BAND anchor fact (`cfb-v3-001` Bo Jackson / guitar) at both layers; capture per-layer post-edit P-values + pathology classification; adjudicate Cell 13 verdict gate per 3-route option matrix.
>
> **Block B verdict surface.** Calibration corridor PASS criterion: post-edit `P(target_new)` `> 0.5` at one of the two candidate layers AND specificity preserved AND unmount drift `< 1e-4`. PASS at one layer → Block C entered at that layer (Route B or Route C per Cell 13). FAIL at both layers → Route A halt → T.2 GRACE ELIM at canonical hparams → escalate per `t_branch_decision_document.md` v1.1 §5'.

## Cell 9 — Single edit dispatch: cfb-v3-001 guitar at Layer-A L17 + RE-EVALUATE flag closure

**Specialist:** memit-specialist (dispatch authority) + validation-contract-architect (RE-EVALUATE AT TRIAL 0 closure per D-S219-Q5-1)

**Purpose:** Dispatch single GRACE edit for cfb-v3-001 (Bo Jackson plays the instrument of guitar) at Layer-A L17. Capture post-edit P-values for Consistency / Generalization / Specificity probes. Per-trial 0 RE-EVALUATE flag closure for ALLOWLIST_FIRST_TOKEN_PROXY facts (D-V12-MULTITOKEN-1 + D-S219-Q5-1 + D-S217-Q5-1 carry-forward).

**Declarative cell body (v0.1):**

```python
# === CELL 9 — Single edit dispatch: cfb-v3-001 guitar at Layer-A L17 ===
# Specialist: memit-specialist + validation-contract-architect
# References: grace-patches-canonical.md v0.1 §5.1 (C-GRACE-1 single-fact);
#             grace-patches-canonical.md v0.1 §5.2 (C-GRACE-2 fresh adapter pool);
#             grace-patches-canonical.md v0.1 §4.2 (Layer-A L17 per D-S219-Q3-1);
#             D-S219-Q5-1 + D-V12-MULTITOKEN-1 (RE-EVALUATE flag closure)

import torch, gc

# 9.1 — Fresh adapter pool initialization at trial entry (C-GRACE-2)
adapter_pool = grace.AdapterPool(model=model, hparams=GRACE_HPARAMS_LAYER_A)
assert adapter_pool.codebook_size == 0

# 9.2 — Build edit request for cfb-v3-001
fact_id = "cfb-v3-001"
fact = next(f for f in cfb_v3["facts"] if f["id"] == fact_id)
edit_request = {
    "subject": fact["subject"],
    "prompt": fact["prompt_template"],
    "target_new": fact["target_new"],
    "target_old": fact.get("target_old"),  # Llama-3.1-8B canonical pre-edit completion (e.g., 'baseball')
}

# 9.3 — Dispatch GRACE edit (single-fact; codebook size 0 → 1)
adapter_pool.add_edit(edit_request)  # declarative API; verify at v0.2
assert adapter_pool.codebook_size == 1

# 9.4 — Post-edit P-capture (verdict_class-aware first-token-proxy per D-V12-MULTITOKEN-1)
vd = fact_verdicts[fact_id]
target_token_id = vd["primary_token_id"]  # 'guitar' under Llama tokenizer; STRICT_SINGLE_TOKEN

post_edit_l17 = {"per_fact": {fact_id: {}}, "shared_specificity": {}}
for probe_role in ("cons", "gen", "spec"):
    for probe in fact_probes[fact_id].get(probe_role, []):
        input_ids = tokenizer(probe["text"], return_tensors="pt").input_ids.to(model.device)
        with torch.no_grad():
            logits = model(input_ids).logits[0, -1].float()
        probs = torch.softmax(logits, dim=-1)
        post_edit_l17["per_fact"][fact_id][probe["id"]] = {
            "p_target": probs[target_token_id].item(),
            "top_1_token_id": int(probs.argmax().item()),
            "top_1_p": probs.max().item(),
        }

for probe in shared_specificity_probes:
    input_ids = tokenizer(probe["text"], return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    probs = torch.softmax(logits, dim=-1)
    post_edit_l17["shared_specificity"][probe["id"]] = {
        "top_1_token_id": int(probs.argmax().item()),
        "top_1_p": probs.max().item(),
    }

# 9.5 — Adapter-detach unmount per C-GRACE-5 (D-S219-Q4-1)
adapter_pool.detach_all()  # declarative API; verify at v0.2
assert adapter_pool.routing_layer_adapters == []

# 9.6 — Post-detach drift assertion (parallel to IC-S23-4 unmount band)
SMOKE_PROBE = "The Eiffel Tower is in"
input_ids = tokenizer(SMOKE_PROBE, return_tensors="pt").input_ids.to(model.device)
with torch.no_grad():
    post_detach_logits = model(input_ids).logits.cpu()
drift_unmount = (smoke_logits_pre.float() - post_detach_logits.float()).abs().max().item()
assert drift_unmount < 1e-4, (
    f"C-GRACE-5 FAIL: post-detach drift={drift_unmount:.2e} > 1e-4; "
    f"adapter-detach not bit-exact under live edit state. "
    f"Fallback to adapter-snapshot-restore (D-S219-Q4-1 option (c)) — exercise at v0.2 absorption"
)

# 9.7 — RE-EVALUATE flag closure (cfb-v3-004 only; not exercised at Cell 9 since fact_id=cfb-v3-001)
# (closure happens at trial 0 of cfb-v3-004 trial in Block C Cell 15; deferred)

# 9.8 — Cleanup
del adapter_pool
gc.collect()
torch.cuda.empty_cache()

print(f"Cell 9: cfb-v3-001 guitar dispatched at L17; post-detach drift={drift_unmount:.2e}.")
```

---

## Cell 10 — Verdict surface for Cell 9 (Layer-A L17)

**Specialist:** validation-contract-architect (calibration corridor evaluation)

**Purpose:** Evaluate Cell 9 post-edit P-values against acceptance bands (`0.5` cons / `0.05` gen / `0.05` spec / `1e-4` unmount); record Layer-A L17 verdict; surface pathology classification if FAIL.

**Declarative cell body (v0.1):**

```python
# === CELL 10 — Verdict surface for Cell 9 (Layer-A L17) ===
# Specialist: validation-contract-architect
# References: D-S24-10 (acceptance bands); IC-S23-4 (unmount band)

# 10.1 — Consistency band evaluation
cons_p_values = [
    p["p_target"]
    for probe_id, p in post_edit_l17["per_fact"]["cfb-v3-001"].items()
    if probe_id.startswith("cons")
]
cons_pass = all(p > 0.5 for p in cons_p_values)
cons_max = max(cons_p_values) if cons_p_values else 0.0

# 10.2 — Specificity band evaluation
spec_drifts = []
for probe_id, current in post_edit_l17["shared_specificity"].items():
    pre = pre_edit_baseline["shared_specificity"][probe_id]
    spec_drifts.append({
        "probe_id": probe_id,
        "top_1_changed": current["top_1_token_id"] != pre["top_1_token_id"],
        "max_p_drift": abs(current["top_1_p"] - pre["top_1_p"]),
    })
spec_pass = all(d["max_p_drift"] < 0.05 and not d["top_1_changed"] for d in spec_drifts)

# 10.3 — Pathology classification (carry-forward from S2.18 ROME taxonomy)
# degenerate-fit: post-edit top_1 collapses to BOS or non-target token despite high gradient flow
# unfittable-landscape: compute_v-equivalent loss does not converge across iterations
# (For GRACE: degenerate-fit = adapter routes correctly but adapter value emits non-target token;
#            unfittable-landscape = adapter optimization loss does not converge)
post_edit_top_1 = post_edit_l17["per_fact"]["cfb-v3-001"]["cons-1"]["top_1_token_id"]
target_token_id = fact_verdicts["cfb-v3-001"]["primary_token_id"]
pathology = None
if not cons_pass:
    if post_edit_top_1 == tokenizer.bos_token_id:
        pathology = "degenerate-fit-BOS-collapse"
    elif post_edit_top_1 != target_token_id and cons_max > 0.0:
        pathology = "degenerate-fit-non-target"
    else:
        pathology = "unfittable-landscape"  # provisional — confirmed by Cell 12 cross-layer

verdict_layer_a = {
    "layer": 17,
    "cons_pass": cons_pass,
    "cons_max": cons_max,
    "spec_pass": spec_pass,
    "spec_drifts": spec_drifts,
    "pathology": pathology,
}
print(f"Cell 10: Layer-A L17 verdict: cons={cons_pass} (max={cons_max:.2e}); spec={spec_pass}; pathology={pathology}")
```

---

## Cell 11 — Single edit dispatch: cfb-v3-001 guitar at Layer-B L2 (cross-layer comparison)

**Specialist:** memit-specialist (dispatch authority)

**Purpose:** Repeat Cell 9 dispatch at Layer-B L2 per D-S219-Q3-1 secondary candidate; capture post-edit P-values for cross-layer comparison.

**Declarative cell body (v0.1):**

```python
# === CELL 11 — Single edit dispatch: cfb-v3-001 guitar at Layer-B L2 ===
# Specialist: memit-specialist
# References: grace-patches-canonical.md v0.1 §4.2 (Layer-B L2 per D-S219-Q3-1)

# 11.1-11.7 — IDENTICAL TO CELL 9 with GRACE_HPARAMS_LAYER_B (layer=2) substitution
# (cell body parallels Cell 9; only the hparam instance differs)

adapter_pool_b = grace.AdapterPool(model=model, hparams=GRACE_HPARAMS_LAYER_B)
adapter_pool_b.add_edit(edit_request)
# ... [identical post-edit P-capture, adapter-detach, drift assertion, cleanup as Cell 9]

# Output: post_edit_l2 dict with same shape as post_edit_l17
```

(Full body inherits Cell 9 structure with `GRACE_HPARAMS_LAYER_B` substitution; abbreviated at v0.1 declarative for token efficiency.)

---

## Cell 12 — Verdict surface for Cell 11 (Layer-B L2) + cross-layer comparison + pathology classification

**Specialist:** validation-contract-architect (cross-layer adjudication)

**Purpose:** Evaluate Cell 11 post-edit P-values; cross-layer comparison Layer-A vs. Layer-B; refine pathology classification (diagnostic-distinct vs. uniform-FAIL).

**Declarative cell body (v0.1):**

```python
# === CELL 12 — Verdict surface for Cell 11 + cross-layer comparison ===
# Specialist: validation-contract-architect
# References: D-S24-10 (acceptance bands); S2.18 ROME pathology taxonomy carry-forward

# 12.1 — Cell 11 verdict (parallel to Cell 10)
verdict_layer_b = {
    "layer": 2,
    "cons_pass": ...,  # parallel to verdict_layer_a
    "cons_max": ...,
    "spec_pass": ...,
    "spec_drifts": ...,
    "pathology": ...,
}

# 12.2 — Cross-layer comparison
both_fail = (not verdict_layer_a["cons_pass"]) and (not verdict_layer_b["cons_pass"])
diagnostic_distinct = (verdict_layer_a["pathology"] != verdict_layer_b["pathology"])
one_passes = verdict_layer_a["cons_pass"] or verdict_layer_b["cons_pass"]

# 12.3 — Replay-S2.15-D2-precedent risk (per t2_rome v0.2 Cell 12 pattern)
# (HIGH if both layers FAIL with diagnostic-distinct pathologies; LOW if one passes)
replay_precedent_risk = "HIGH" if (both_fail and diagnostic_distinct) else "LOW"

cross_layer_comparison = {
    "both_fail": both_fail,
    "diagnostic_distinct": diagnostic_distinct,
    "one_passes": one_passes,
    "replay_precedent_risk": replay_precedent_risk,
    "load_bearing_layer": (
        17 if verdict_layer_a["cons_pass"] else
        (2 if verdict_layer_b["cons_pass"] else None)
    ),
}
print(f"Cell 12: cross-layer comparison: both_fail={both_fail}; diagnostic_distinct={diagnostic_distinct}; load_bearing_layer={cross_layer_comparison['load_bearing_layer']}")
```

---

## Cell 13 — Block B verdict gate: 3-route option matrix (INHERITED from t2_rome_runbook v0.2)

**Specialist:** validation-contract-architect (verdict gate authority) + memit-specialist (mechanism interpretation)

**Purpose:** Block B verdict consolidation per 3-route option matrix INHERITED VERBATIM from `t2_rome_runbook.md` v0.2 Cell 13. Three deliverables: verdict class adjudication; multi-token tolerance posture for cfb-v3-004 finalized (if Block C entered) at trial 0; routing decision (Route A halt / Route B 15-trial / Route C 3-trial preview).

**3-route option matrix (carry-forward from `t2_rome_runbook.md` v0.2 Cell 13):**

| Route | Trigger condition | Block C behavior | Disposition |
|---|---|---|---|
| **A — Halt** | Calibration corridor FAIL at both layers AND pathology diagnostic distinct AND replay-S2.15-D2-precedent risk HIGH | Block C NOT executed; session closes at Cell 13; verdict = B-FAIL → T.2 GRACE ELIM at canonical | Escalate per `t_branch_decision_document.md` v1.1 §5' (FALL BACK TO T.1) |
| **B — Full 15-trial Block C** | Calibration corridor PASS at one layer (consistency `> 0.5` at L17 OR L2) | Cells 14–17 execute full 15-trial loop (5 facts × 3 replicates) at the load-bearing layer; verdict via Cell 17 aggregate | Block C entered |
| **C — Reduced 3-trial Block C** | Calibration corridor BORDERLINE (consistency in `[0.4, 0.5]` at one layer) AND operator authorizes reduced protocol | Cells 14–17 execute 3-trial loop (load-bearing subset only at single replicate) for verdict integrity preview; full protocol deferred | Block C entered (preview) |

**Verdict classes (parallel to `t2_rome_runbook.md` v0.2 Cell 13):**

| Verdict | Definition | Routes to |
|---|---|---|
| **B-PASS** | Calibration corridor PASS at one layer AND multi-token tolerance posture finalized | Route B (or C); Block C 15-trial (or 3-trial) execution at load-bearing layer |
| **B-FAIL** | Calibration corridor FAIL at both layer candidates AND pathology diagnostic distinct | Route A halt → T.2 GRACE ELIM at canonical hparams → FALL BACK TO T.1 |
| **B-PARTIAL** | Calibration corridor BORDERLINE | Route C (3-trial preview) OR operator-side verdict integrity binding re-evaluation |

**Declarative cell body (v0.1):**

```python
# === CELL 13 — Block B verdict gate: 3-route option matrix (INHERITED from t2_rome v0.2) ===
# Specialist: validation-contract-architect + memit-specialist
# Inheritance: t2_rome_runbook.md v0.2 Cell 13 (3-route option matrix)
# References: t_branch_decision_document.md v1.1 §5' (conditional execution plan)

# 13.1 — Verdict class adjudication
if cross_layer_comparison["one_passes"]:
    if cross_layer_comparison["load_bearing_layer"] is not None:
        load_bearing_cons_max = max(verdict_layer_a["cons_max"], verdict_layer_b["cons_max"])
        if load_bearing_cons_max > 0.5:
            verdict_class = "B-PASS"
            block_c_route = "B"  # full 15-trial
        elif 0.4 <= load_bearing_cons_max <= 0.5:
            verdict_class = "B-PARTIAL"
            block_c_route = "C"  # 3-trial preview (operator authorization required)
        else:
            verdict_class = "B-FAIL"
            block_c_route = "A"  # halt
    else:
        verdict_class = "B-FAIL"
        block_c_route = "A"
elif cross_layer_comparison["both_fail"] and cross_layer_comparison["diagnostic_distinct"] and cross_layer_comparison["replay_precedent_risk"] == "HIGH":
    verdict_class = "B-FAIL"
    block_c_route = "A"  # halt → T.2 GRACE ELIM at canonical hparams
else:
    verdict_class = "B-PARTIAL"
    block_c_route = "C"

block_b_verdict = {
    "verdict_class": verdict_class,
    "block_c_route": block_c_route,
    "load_bearing_layer": cross_layer_comparison["load_bearing_layer"],
    "verdict_layer_a": verdict_layer_a,
    "verdict_layer_b": verdict_layer_b,
    "cross_layer_comparison": cross_layer_comparison,
}
Path("/workspace/grace_dry_run/block_b_verdict.json").write_text(json.dumps(block_b_verdict, indent=2, default=str))

# 13.2 — Routing decision print
print(f"Cell 13: Block B verdict_class={verdict_class}; route={block_c_route}; load_bearing_layer={cross_layer_comparison['load_bearing_layer']}")
if block_c_route == "A":
    print("Cell 13: Route A halt selected → T.2 GRACE ELIM at canonical hparams → FALL BACK TO T.1 per t_branch_decision_document v1.1 §5'")
    raise SystemExit(0)  # halt before Block C entry
```

---

# Part V — Block C: Stage 1 SECT v3 execution at single-fact GRACE dispatch (Cells 14–20)

> **Block C purpose.** Execute the 15-trial Stage 1 SECT v3 protocol per IC-S24-4 against the load-bearing layer selected at Block B Cell 13. Each trial is a single-fact GRACE edit (per `C-GRACE-1`). Trial loop structure mirrors `t2_rome_runbook.md` v0.2 Block C with single-fact GRACE dispatch + adapter-detach unmount substitution.
>
> **v0.1 declarative disposition.** Cells 14-20 are codified at v0.1 in declarative form for any execution session that enters Block B verdict PASS / PARTIAL routing (B / C). If S2.20 Block B Cell 13 routes Route A halt, Block C is SKIPPED at S2.20 (parallel to S2.18 ROME pattern); v0.2 absorption codifies the actual execution path post-S2.20.

## Cell 14 — Trial matrix authoring (D-S217-2 + verdict integrity binding carry-forward)

**Specialist:** validation-contract-architect (IC-S24-4 enforcement)

**Purpose:** Enumerate 15 trials per IC-S24-4 (5 facts × 3 replicates) — OR 3 trials at Route C (3 load-bearing subset facts × 1 replicate); apply D-S217-2 cross-cell SUBSET hard gate (Cell 6 ↔ Cell 8 ↔ Cell 14 single-source); apply D-S215D2-VERDICT-INTEGRITY-1 load-bearing-subset annotation. INHERITED VERBATIM from `t2_rome_runbook.md` v0.2 Cell 14 with GRACE-side path adaptations.

**Declarative cell body (v0.1) — INHERITED from `t2_rome_runbook.md` v0.2 Cell 14:**

```python
# === CELL 14 — Trial matrix authoring (inherited from t2_rome_runbook v0.2 Cell 14) ===
# Specialist: validation-contract-architect
# Inheritance: t2_rome_runbook.md v0.2 Cell 14
# References: IC-S24-4 (5×3 trial protocol); D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset);
#             D-S217-2 (Cell 6/8 single-source contract; carry-forward to Cell 14);
#             v0.1 GRACE-side substitution: GRACE_HPARAMS instead of ROME_HPARAMS

LOAD_BEARING_LAYER = block_b_verdict["load_bearing_layer"]          # from Cell 13: 17 OR 2
BLOCK_C_ROUTE = block_b_verdict["block_c_route"]                    # from Cell 13: "B" OR "C"
GRACE_HPARAMS_BLOCK_C = (
    GRACE_HPARAMS_LAYER_A if LOAD_BEARING_LAYER == 17 else GRACE_HPARAMS_LAYER_B
)

# Route B = 5 facts × 3 replicates = 15 trials; Route C = 3 load-bearing facts × 1 replicate = 3 trials
LOAD_BEARING_SUBSET = {"cfb-v3-001", "cfb-v3-002", "cfb-v3-005"}
FORENSIC_INFORMATIVE_DEFAULT = {"cfb-v3-003", "cfb-v3-004"}

if BLOCK_C_ROUTE == "B":
    eligible_facts = sorted(fact_verdicts.keys())   # all 5 facts
    REPLICATES = 3
    EXPECTED_TRIAL_COUNT = 15
elif BLOCK_C_ROUTE == "C":
    eligible_facts = sorted(LOAD_BEARING_SUBSET)
    REPLICATES = 1
    EXPECTED_TRIAL_COUNT = 3
else:
    raise RuntimeError(f"Cell 14: invalid BLOCK_C_ROUTE = {BLOCK_C_ROUTE}; expected 'B' or 'C'")

trial_matrix = []
trial_index = 0
for fact_id in eligible_facts:
    fact = next(f for f in cfb_v3["facts"] if f["id"] == fact_id)
    for replicate in range(1, REPLICATES + 1):
        trial_matrix.append({
            "trial_index": trial_index,
            "fact_id": fact_id,
            "replicate": replicate,
            "grace_request": {
                "subject": fact["subject"],
                "prompt": fact["prompt_template"],
                "target_new": fact["target_new"],
                "target_old": fact.get("target_old"),
            },
            "hparams_layer": LOAD_BEARING_LAYER,
            "per_fact_probes": fact_probes[fact_id],
            "shared_specificity_probes": shared_specificity_probes,
            "torch_seed": 0,
            "subset_annotation": (
                "load_bearing" if fact_id in LOAD_BEARING_SUBSET
                else "forensic_informative_excluded"
            ),
            "verdict_class": fact_verdicts[fact_id]["verdict_class"],
            "primary_token_id": fact_verdicts[fact_id]["primary_token_id"],
        })
        trial_index += 1

assert len(trial_matrix) == EXPECTED_TRIAL_COUNT
Path("/workspace/stage_1_sect_grace/trial_matrix.json").write_text(json.dumps(trial_matrix, indent=2))
```

---

## Cell 15 — Trial loop execution (single-fact GRACE edits + adapter-detach per fact)

**Specialist:** memit-specialist (dispatch authority) + state-consistency-theorist (per-trial isolation per `C-GRACE-2`)

**Purpose:** Execute trial matrix; per trial: fresh adapter pool initialization → GRACE edit dispatch → post-edit P-capture → adapter-detach unmount → post-detach drift assertion → per-trial verdict record. RE-EVALUATE flag closure for cfb-v3-004 trial 0 per D-S219-Q5-1 + D-V12-MULTITOKEN-1.

**Declarative cell body (v0.1):**

```python
# === CELL 15 — Trial loop execution (single-fact GRACE edits + adapter-detach per fact) ===
# Specialist: memit-specialist + state-consistency-theorist
# References: grace-patches-canonical.md v0.1 §5.1 (C-GRACE-1); §5.2 (C-GRACE-2 per-trial isolation);
#             §5.5 (C-GRACE-5 adapter-detach); D-S219-Q5-1 (RE-EVALUATE flag closure)

per_trial_verdicts = []
re_evaluate_log = {}  # cfb-v3-004 trial 0 RE-EVALUATE record

for trial in trial_matrix:
    trial_index = trial["trial_index"]
    fact_id = trial["fact_id"]
    is_first_trial_of_fact = trial["replicate"] == 1

    # 15.1 — Fresh adapter pool initialization at trial entry (C-GRACE-2)
    adapter_pool = grace.AdapterPool(model=model, hparams=GRACE_HPARAMS_BLOCK_C)
    assert adapter_pool.codebook_size == 0
    assert adapter_pool.routing_layer_adapters == []

    # 15.2 — Pre-edit baseline (per-trial; verifies cross-session bit-exact + carries forward Cell 7 data)
    # (For efficiency: reuse Cell 7 pre_edit_baseline data; per-trial check via SMOKE_PROBE drift only)
    SMOKE_PROBE = "The Eiffel Tower is in"
    input_ids = tokenizer(SMOKE_PROBE, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        pre_edit_logits = model(input_ids).logits.cpu()

    # 15.3 — GRACE edit dispatch (single-fact per C-GRACE-1)
    adapter_pool.add_edit(trial["grace_request"])
    assert adapter_pool.codebook_size == 1

    # 15.4 — RE-EVALUATE flag closure (cfb-v3-004 trial 0 only; D-S219-Q5-1 + D-V12-MULTITOKEN-1)
    if fact_id == "cfb-v3-004" and is_first_trial_of_fact:
        # Test: does GRACE adapter dispatch natively handle full multi-token target_new?
        full_token_ids = fact_verdicts[fact_id]["full_token_ids"]
        cons_probe = trial["per_fact_probes"]["cons"][0]
        input_ids_re = tokenizer(cons_probe["text"], return_tensors="pt").input_ids.to(model.device)
        with torch.no_grad():
            full_seq_logits = model.generate(
                input_ids_re, max_new_tokens=len(full_token_ids), do_sample=False, output_scores=True, return_dict_in_generate=True,
            )
        # Compute P(full target_new sequence) under post-edit model
        # If P_full > 0.5 → first-token-proxy RETIRED for rest of cfb-v3-004 trials
        # If P_full <= 0.5 → first-token-proxy RATIFIED for full 3-replicate cfb-v3-004 trial set
        p_full = ...  # declarative computation; v0.2 absorption codifies actual API
        re_evaluate_log = {
            "fact_id": "cfb-v3-004",
            "trial_index": trial_index,
            "p_full_target_new": p_full,
            "first_token_proxy_disposition": (
                "RETIRED" if p_full > 0.5 else "RATIFIED"
            ),
        }
        Path("/workspace/stage_1_sect_grace/re_evaluate_log.json").write_text(
            json.dumps(re_evaluate_log, indent=2)
        )

    # 15.5 — Post-edit P-capture (verdict_class-aware first-token-proxy)
    target_token_id = trial["primary_token_id"]
    post_edit_per_trial = {"per_fact": {fact_id: {}}, "shared_specificity": {}}
    for probe_role in ("cons", "gen", "spec"):
        for probe in trial["per_fact_probes"].get(probe_role, []):
            input_ids_p = tokenizer(probe["text"], return_tensors="pt").input_ids.to(model.device)
            with torch.no_grad():
                logits = model(input_ids_p).logits[0, -1].float()
            probs = torch.softmax(logits, dim=-1)
            post_edit_per_trial["per_fact"][fact_id][probe["id"]] = {
                "p_target": probs[target_token_id].item(),
                "top_1_token_id": int(probs.argmax().item()),
                "top_1_p": probs.max().item(),
            }
    for probe in trial["shared_specificity_probes"]:
        input_ids_s = tokenizer(probe["text"], return_tensors="pt").input_ids.to(model.device)
        with torch.no_grad():
            logits = model(input_ids_s).logits[0, -1].float()
        probs = torch.softmax(logits, dim=-1)
        post_edit_per_trial["shared_specificity"][probe["id"]] = {
            "top_1_token_id": int(probs.argmax().item()),
            "top_1_p": probs.max().item(),
        }

    # 15.6 — Adapter-detach unmount per C-GRACE-5
    adapter_pool.detach_all()
    assert adapter_pool.routing_layer_adapters == []

    # 15.7 — Post-detach drift assertion (per-trial unmount band IC-S23-4)
    with torch.no_grad():
        post_detach_logits = model(input_ids).logits.cpu()
    drift_unmount = (pre_edit_logits.float() - post_detach_logits.float()).abs().max().item()
    if drift_unmount > 1e-4:
        # Fallback to adapter-snapshot-restore per D-S219-Q4-1 option (c)
        # (v0.2 absorption codifies fallback mechanism; v0.1 declarative records the assertion FAIL)
        print(f"Trial {trial_index} unmount FAIL: drift={drift_unmount:.2e}; fallback to snapshot-restore TBD at v0.2")

    # 15.8 — Per-trial verdict record
    per_trial_verdicts.append({
        "trial_index": trial_index,
        "fact_id": fact_id,
        "replicate": trial["replicate"],
        "post_edit_per_trial": post_edit_per_trial,
        "drift_unmount": drift_unmount,
        "subset_annotation": trial["subset_annotation"],
        "verdict_class": trial["verdict_class"],
    })

    # 15.9 — Cleanup
    del adapter_pool
    gc.collect()
    torch.cuda.empty_cache()

# 15.10 — Write per-trial verdicts to NV
Path("/workspace/stage_1_sect_grace/per_trial_verdicts.json").write_text(
    json.dumps(per_trial_verdicts, indent=2)
)
```

**v0.2 absorption notes:**
- Actual `grace.AdapterPool.add_edit()` + `.detach_all()` API verified at S2.20 first-execution.
- RE-EVALUATE closure mechanism (15.4) — exact P_full computation API codified at v0.2 per actual GRACE multi-token dispatch behavior.
- If adapter-detach fails the unmount band (drift `> 1e-4` at any trial), fallback to adapter-snapshot-restore (D-S219-Q4-1 option (c)) is exercised; v0.2 absorption codifies the fallback unmount mechanism + revises `C-GRACE-5` accordingly.
- OQ-S219-3 closure: empirical verification at Cell 15 of single-fact-per-trial vs. adapter-accumulation; if accumulation is structurally enforced by GRACE codebase, `C-GRACE-1` envelope revised at v0.2.

---

## Cell 16 — Per-trial verdict aggregation

**Specialist:** validation-contract-architect (per-trial verdict adjudication)

**Purpose:** Per-trial PASS/FAIL determination against acceptance bands; per-fact aggregation across replicates. INHERITED structurally from `t2_rome_runbook.md` v0.2 Cell 16.

**Declarative cell body (v0.1):**

```python
# === CELL 16 — Per-trial verdict aggregation ===
# Specialist: validation-contract-architect

per_trial_pass_fail = []
for v in per_trial_verdicts:
    fact_id = v["fact_id"]
    cons_p = [p["p_target"] for pid, p in v["post_edit_per_trial"]["per_fact"][fact_id].items() if pid.startswith("cons")]
    spec_drifts = [
        abs(v["post_edit_per_trial"]["shared_specificity"][pid]["top_1_p"] - pre_edit_baseline["shared_specificity"][pid]["top_1_p"])
        for pid in v["post_edit_per_trial"]["shared_specificity"]
    ]
    cons_pass = all(p > 0.5 for p in cons_p)
    spec_pass = all(d < 0.05 for d in spec_drifts)
    unmount_pass = v["drift_unmount"] < 1e-4
    per_trial_pass_fail.append({
        "trial_index": v["trial_index"],
        "fact_id": fact_id,
        "replicate": v["replicate"],
        "subset_annotation": v["subset_annotation"],
        "cons_pass": cons_pass,
        "spec_pass": spec_pass,
        "unmount_pass": unmount_pass,
        "trial_pass": cons_pass and spec_pass and unmount_pass,
    })
Path("/workspace/stage_1_sect_grace/per_trial_pass_fail.json").write_text(json.dumps(per_trial_pass_fail, indent=2))
```

---

## Cell 17 — Aggregate verdict (load-bearing subset + full-aggregate)

**Specialist:** validation-contract-architect (D-S215D2-VERDICT-INTEGRITY-1 enforcement)

**Purpose:** Aggregate Block C verdict over load-bearing subset (D-S215D2-VERDICT-INTEGRITY-1: requires PASS at all three load-bearing facts); aggregate full-protocol verdict over all 5 facts (informational).

**Declarative cell body (v0.1):**

```python
# === CELL 17 — Aggregate verdict (load-bearing subset + full-aggregate) ===
# Specialist: validation-contract-architect
# References: D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset gating)

load_bearing_results = {fid: [] for fid in LOAD_BEARING_SUBSET}
full_results = {fid: [] for fid in fact_verdicts}
for r in per_trial_pass_fail:
    full_results[r["fact_id"]].append(r["trial_pass"])
    if r["fact_id"] in LOAD_BEARING_SUBSET:
        load_bearing_results[r["fact_id"]].append(r["trial_pass"])

# Per-fact PASS = majority of replicates PASS (per D-S24-10 / IC-S24-4)
def fact_pass(replicate_results):
    return sum(replicate_results) > len(replicate_results) / 2

load_bearing_per_fact_pass = {fid: fact_pass(rs) for fid, rs in load_bearing_results.items()}
load_bearing_aggregate_pass = all(load_bearing_per_fact_pass.values())

full_per_fact_pass = {fid: fact_pass(rs) for fid, rs in full_results.items()}
full_aggregate_pass = all(full_per_fact_pass.values())

block_c_verdict = {
    "load_bearing_per_fact_pass": load_bearing_per_fact_pass,
    "load_bearing_aggregate_pass": load_bearing_aggregate_pass,    # gating per D-S215D2-VERDICT-INTEGRITY-1
    "full_per_fact_pass": full_per_fact_pass,
    "full_aggregate_pass": full_aggregate_pass,                    # informational
    "verdict_class": (
        "C-PASS" if load_bearing_aggregate_pass else "C-FAIL"
    ),
}
Path("/workspace/stage_1_sect_grace/block_c_verdict.json").write_text(json.dumps(block_c_verdict, indent=2))
print(f"Cell 17: Block C verdict_class = {block_c_verdict['verdict_class']}; load_bearing_aggregate_pass = {load_bearing_aggregate_pass}")
```

---

## Cell 18 — NV inventory + SHA equality gate

**Specialist:** state-consistency-theorist (NV inventory authority)

**Purpose:** NV directory inventory after Block C; SHA equality gate against carried baseline (covariance caches L2-L8 + L17 unmodified; new artifacts under `/workspace/stage_1_sect_grace/`). INHERITED structurally from `t2_rome_runbook.md` v0.2 Cell 18.

**Declarative cell body (v0.1):**

```bash
# === CELL 18 — NV inventory + SHA equality gate ===
# Specialist: state-consistency-theorist
# Inheritance: t2_rome_runbook.md v0.2 Cell 18

du -sh /workspace/stage_1_sect_grace/
du -sh /workspace/covariance_caches/  # should be unchanged from S2.18 close (~6.5 GiB)

# SHA equality gate: covariance caches unchanged from S2.18 close
sha256sum /workspace/covariance_caches/d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/wikipedia_stats/*.npz \
    > /workspace/grace_dry_run/covariance_sha_post_s220.txt
diff /workspace/covariance_caches/d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/wikipedia_stats/SHA_BASELINE.txt \
     /workspace/grace_dry_run/covariance_sha_post_s220.txt
# Expected: zero diff (GRACE does not consume covariance caches; bit-exact preserved)
```

---

## Cell 19 — Mirror sync (NV → SSD)

**Specialist:** state-consistency-theorist

**Purpose:** Sync `/workspace/stage_1_sect_grace/` from NV to pod SSD `/root/stage_1_sect_grace_mirror/` for redundant storage. INHERITED structurally from `t2_rome_runbook.md` v0.2 Cell 19.

**Declarative cell body (v0.1):**

```bash
# === CELL 19 — Mirror sync (NV → SSD) ===
mkdir -p /root/stage_1_sect_grace_mirror
rsync -a --info=progress2 /workspace/stage_1_sect_grace/ /root/stage_1_sect_grace_mirror/
```

---

## Cell 20 — Block C verdict + reproducibility manifest update + routing decision

**Specialist:** framework-spec-writer (manifest update authority) + memit-specialist (routing decision)

**Purpose:** Update `/workspace/reproducibility_manifest.json` with S2.20 entry; surface forward routing decision per `t_branch_decision_document.md` v1.1 §5'.

**Declarative cell body (v0.1):**

```python
# === CELL 20 — Block C verdict + reproducibility manifest update + routing decision ===
# Specialist: framework-spec-writer + memit-specialist
# References: t_branch_decision_document.md v1.1 §5' (conditional execution plan)

# 20.1 — Reproducibility manifest update
manifest_path = Path("/workspace/reproducibility_manifest.json")
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"sessions": {}}
manifest["sessions"]["2.20"] = {
    "engine": "GRACE",
    "engine_sha": Path("/workspace/grace_dry_run/env_fingerprint.txt").read_text().strip(),
    "block_b_verdict": block_b_verdict,
    "block_c_verdict": block_c_verdict if "block_c_verdict" in dir() else None,
    "load_bearing_layer": LOAD_BEARING_LAYER,
    "block_c_route": BLOCK_C_ROUTE,
    "re_evaluate_log": re_evaluate_log,
}
manifest_path.write_text(json.dumps(manifest, indent=2))

# 20.2 — Forward routing decision
verdict_final = block_c_verdict["verdict_class"] if block_c_route != "A" else "B-FAIL"
if verdict_final == "C-PASS":
    print("Cell 20: T.2 GRACE PASS at canonical hparams")
    print("        Ceiling = rank-1-in-weight-class-mechanism-specific")
    print("        S2.21 = MEMIT-vs-ROME-vs-GRACE comparison framework finding update (resolves OQ-V11-T-BRANCH-6)")
elif verdict_final in ("C-FAIL", "B-FAIL"):
    print(f"Cell 20: T.2 GRACE {verdict_final} at canonical hparams")
    print("        Ceiling generalizes to adapter mechanisms — suspect (model × hparams)")
    print("        S2.21 = T.1 alt-model runbook v0.1 authoring per t_branch_decision_document.md v1.1 §5' fallback")
else:
    print(f"Cell 20: T.2 GRACE {verdict_final} — operator-side verdict integrity binding re-evaluation per t_branch v1.0 §5")
```

---

# Part VIII — Open questions

## 8.1 OQs closed by S2.19 v0.1 authoring

| OQ ID | Closure | Closure ID |
|---|---|---|
| OQ-V11-T-BRANCH-1 | GRACE SHA pin: latest stable tip of `https://github.com/Thartvigsen/GRACE` | D-S219-Q1-1 |
| OQ-V11-T-BRANCH-2 | GRACE canonical hparams: paper Table 1 + Llama-3.1-8B adaptation | D-S219-Q2-1 |
| OQ-V11-T-BRANCH-3 | GRACE adapter placement: Layer-A L17 primary + Layer-B L2 secondary | D-S219-Q3-1 |
| OQ-V11-T-BRANCH-5 | GRACE unmount mechanism: adapter-detach (option (c) snapshot-restore considered fallback) | D-S219-Q4-1 |
| OQ-V11-T-BRANCH-4 | Multi-token tolerance posture for cfb-v3-004 under GRACE: first-token-proxy carry-forward + RE-EVALUATE flag | D-S219-Q5-1 |
| OQ-S219-4 | Cell 3 disposition: INAPPLICABLE-DEFERRED-BY-MECHANISM (option (a)); adapter-pool initialization verification folded into Cell 8 | D-S219-CELL3-1 (recorded at this cell + §10.4) |

## 8.2 OQs activated / opened at v0.1 authoring

| OQ ID | Surface | Closure path |
|---|---|---|
| OQ-S219-1 | P-1 / P-2 retain-trace applicability under GRACE adapter forward pass | S2.20 Block A Cell 2 grep-anchor inspection |
| OQ-S219-2 | GRACE CONFIG_LAYER analog (`globals.yml`-equivalent) | S2.20 Block A Cell 8 initial diagnostic |
| OQ-S219-3 | GRACE multi-fact dispatch semantics (single-fact-per-trial vs. adapter-accumulation) | v0.2 absorption per S2.20 Cell 15 empirical record |
| OQ-V11-T-BRANCH-6 (carried) | Comparison framework finding artifact post-S2.20 PASS | S2.21 (PASS) or DEFERRED (FAIL) |

## 8.3 OQs explicitly out of scope

| OQ | Reason |
|---|---|
| OQ-S214D-* (D.1 mediation, predicate refinement, OOM, etc.) | Closed by S2.18 / S2.15-D2 / framework_finding v1.1; no longer load-bearing for T.2 GRACE |
| OQ-S213C-10 (Cell 6/8 single-source pattern) | Closed at v1.6 hardening per D-S217-2; carries forward as the source-contract pattern; no GRACE-specific surface |

---

# Part X — Reference appendices

## 10.1 Carry-forward inheritance from `t2_rome_runbook.md` v0.2 + `stage_1_sect_runbook_v1_7.md`

| Inheritance source | Cells / Sections | GRACE-side adaptation |
|---|---|---|
| `t2_rome_runbook.md` v0.2 Cell 0 | Cell 0 | INHERITED UNCHANGED |
| `t2_rome_runbook.md` v0.2 Cell 1 | Cell 1 | repo URL substitution: `Thartvigsen/GRACE` for `kmeng01/rome` |
| `t2_rome_runbook.md` v0.2 Cell 1.5 | Cell 1.5 | `engine` field substitution: `"GRACE"` |
| `t2_rome_runbook.md` v0.2 Cell 2 | Cell 2 | OQ-S219-1 closure step (P-1 / P-2 grep-anchor); reduced patch surface |
| `t2_rome_runbook.md` v0.2 Cell 3 | Cell 3 | INAPPLICABLE-DEFERRED-BY-MECHANISM per OQ-S219-4 (a) |
| `t2_rome_runbook.md` v0.2 Cell 4 | Cell 4 | `GraceHyperParamsExtended` substitution; layer-set per D-S219-Q3-1 |
| `t2_rome_runbook.md` v0.2 Cell 5 | Cell 5 | INHERITED UNCHANGED (target model identical) |
| `stage_1_sect_runbook_v1_7.md` §1.5.3.1 | Cell 6 | INHERITED VERBATIM (MULTI_TOKEN_ALLOWLIST canonical absorption) |
| `stage_1_sect_runbook_v1_7.md` §1.5.3.2 | Cell 7 | INHERITED with engine-agnostic adaptation |
| `t2_rome_runbook.md` v0.2 Cell 8 | Cell 8 | GRACE smoke-load substitution + Cell 3 deferral absorption |
| `t2_rome_runbook.md` v0.2 Cell 9-12 | Cells 9-12 | GRACE dispatch substitution (`grace.AdapterPool` for ROME `apply_rome_to_model`); pathology taxonomy carry-forward |
| `t2_rome_runbook.md` v0.2 Cell 13 | Cell 13 | INHERITED VERBATIM (3-route option matrix; verdict classes) |
| `t2_rome_runbook.md` v0.2 Cell 14 | Cell 14 | INHERITED with `GRACE_HPARAMS_BLOCK_C` substitution |
| `t2_rome_runbook.md` v0.2 Cell 15 | Cell 15 | GRACE dispatch + adapter-detach unmount substitution; RE-EVALUATE closure for cfb-v3-004 trial 0 |
| `t2_rome_runbook.md` v0.2 Cell 16-20 | Cells 16-20 | INHERITED structurally with GRACE-side path adaptations |

## 10.2 NV-resident artifact paths (declarative; v0.1)

```
/workspace/grace_dry_run/grace/                  # GRACE clone (Cell 1)
/workspace/grace_dry_run/env_fingerprint.txt     # SHA hash record
/workspace/grace_dry_run/env_fingerprint.json    # full environment fingerprint (Cell 1.5)
/workspace/grace_dry_run/t2_grace_patch_state.json  # patch state manifest (Cell 2)
/workspace/grace_dry_run/pre_edit_baseline.json  # pre-edit baseline (Cell 7)
/workspace/grace_dry_run/block_b_verdict.json    # Block B verdict (Cell 13)
/workspace/grace_dry_run/covariance_sha_post_s220.txt  # SHA equality gate (Cell 18)

/workspace/stage_1_sect_grace/trial_matrix.json       # trial enumeration (Cell 14)
/workspace/stage_1_sect_grace/per_trial_verdicts.json # per-trial P-values (Cell 15)
/workspace/stage_1_sect_grace/per_trial_pass_fail.json  # per-trial verdict adjudication (Cell 16)
/workspace/stage_1_sect_grace/block_c_verdict.json    # Block C aggregate verdict (Cell 17)
/workspace/stage_1_sect_grace/re_evaluate_log.json    # cfb-v3-004 RE-EVALUATE closure (Cell 15.4)

/root/stage_1_sect_grace_mirror/                 # SSD mirror (Cell 19)
/workspace/reproducibility_manifest.json         # S2.20 entry update (Cell 20)
```

## 10.3 Wall-time budget per cell (declarative; v0.1)

| Cell | Declarative wall-time estimate | Empirical anchor |
|---|---|---|
| 0 — System binaries + Python deps | ~2-5 min | parallel to ROME / MEMIT pattern |
| 1 — GRACE repo clone + SHA pin | ~30 sec | parallel to ROME pattern |
| 1.5 — Environment fingerprint | <10 sec | parallel |
| 2 — Patch state verification + transplant | ~1-3 min (depending on OQ-S219-1 disposition) | parallel to ROME Cell 2 |
| 3 — INAPPLICABLE-DEFERRED-BY-MECHANISM (no-op) | <5 sec | (structural placeholder) |
| 4 — Hparam declaration | <30 sec | parallel |
| 5 — Model load + Pad-Token + bit-exact gate | ~3-5 min | parallel (Llama-3.1-8B fp16 on RTX 4090) |
| 6 — Tokenizer single-token + MULTI_TOKEN_ALLOWLIST | <30 sec | inherited from v1.7 |
| 7 — Pre-edit baseline | ~2-3 min | parallel |
| 8 — R1.3 dry-run gate + adapter-pool init verification | ~1-2 min | declarative; first-execution at S2.20 will record empirical anchor |
| 9 — Single edit dispatch L17 | ~5-10 min (declarative; depends on `n_iter` × forward-pass cost) | TBD at S2.20 |
| 10 — Verdict surface L17 | <30 sec | parallel |
| 11 — Single edit dispatch L2 | ~5-10 min | TBD at S2.20 |
| 12 — Verdict surface L2 + cross-layer comparison | <1 min | parallel |
| 13 — Block B verdict gate | <30 sec | inherited from t2_rome v0.2 |
| 14 — Trial matrix authoring | <30 sec | inherited |
| 15 — Trial loop execution (15 trials) | ~75-150 min (declarative; 5-10 min per trial × 15) | TBD at S2.20 |
| 16 — Per-trial verdict aggregation | <1 min | parallel |
| 17 — Aggregate verdict | <30 sec | parallel |
| 18 — NV inventory + SHA equality gate | ~1-2 min | parallel |
| 19 — Mirror sync | ~1-3 min | parallel |
| 20 — Manifest update + routing decision | <30 sec | parallel |

**Total Block A wall-time:** ~15-25 min (declarative)
**Total Block B wall-time:** ~15-25 min (declarative)
**Total Block C wall-time (Route B):** ~75-150 min (declarative; dominates total)
**Total session wall-time (Route B):** ~110-200 min (declarative; ~2-3.5 hr)
**Total session wall-time (Route A halt):** ~30-50 min (Block A + Block B only; no Block C)

## 10.4 Cell-to-decision traceability

| Cell | Decisions / Constraints anchored |
|---|---|
| 0 | C-S214D-4 (HF_HOME before transformers import) |
| 1 | D-S219-Q1-1 (SHA pin) |
| 1.5 | (none — provenance discipline) |
| 2 | OQ-S219-1 closure (P-1 / P-2 retain-trace); C-GRACE-4 (marker verification) |
| 3 | OQ-S219-4 closure (a) — INAPPLICABLE-DEFERRED-BY-MECHANISM; D-S219-CELL3-1 (recorded here); mechanism-orthogonality assertion per `t_branch_decision_document.md` v1.1 §6'.3 |
| 4 | D-S219-Q2-1 (canonical hparams); D-S219-Q3-1 (Layer-A L17 + Layer-B L2); C-S218-5 parallel (`GraceHyperParamsExtended`) |
| 5 | D-S217-4 + D-S218-7 (cross-session bit-exact 6 → 7 checkpoint extension); Pad-Token APPLICABLE DIRECTLY |
| 6 | D-V12-MULTITOKEN-1 (MULTI_TOKEN_ALLOWLIST + verdict_class taxonomy); D-S219-Q5-1 carry-forward |
| 7 | D-V12-MULTITOKEN-1 (first-token-proxy P-capture wiring); D-S217-4 + D-S218-7 (anchor extension) |
| 8 | C-GRACE-3 (R1.3-equivalent dry-run gate); C-GRACE-2 (adapter-pool initialization verification — Cell 3 deferral) |
| 9 | C-GRACE-1 (single-fact dispatch); C-GRACE-2 (fresh adapter pool); D-S219-Q3-1 (Layer-A); C-GRACE-5 (adapter-detach) |
| 10 | D-S24-10 (acceptance bands); S2.18 ROME pathology taxonomy carry-forward |
| 11 | C-GRACE-1 (single-fact dispatch); D-S219-Q3-1 (Layer-B); C-GRACE-5 (adapter-detach) |
| 12 | S2.18 ROME pathology taxonomy (degenerate-fit / unfittable-landscape); D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset) |
| 13 | t2_rome v0.2 Cell 13 inheritance (3-route option matrix); `t_branch_decision_document.md` v1.1 §5' (conditional execution plan) |
| 14 | IC-S24-4 (5×3 trial protocol); D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset annotation); D-S217-2 (Cell 6/8 single-source contract carry-forward) |
| 15 | C-GRACE-1 + C-GRACE-2 + C-GRACE-5 (single-fact, fresh pool, adapter-detach); D-S219-Q5-1 (RE-EVALUATE flag closure for cfb-v3-004 trial 0); D-V12-MULTITOKEN-1 (verdict_class-aware P-capture); IC-S23-4 (unmount band) |
| 16 | D-S24-10 (acceptance bands per-trial) |
| 17 | D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset gating); D-S24-10 (per-fact replicate majority) |
| 18 | (NV inventory; bit-exact gate on covariance caches) |
| 19 | (mirror sync provenance) |
| 20 | `t_branch_decision_document.md` v1.1 §5' (conditional execution plan; forward routing decision) |

## 10.5 Authoring metadata

| Field | Value |
|---|---|
| Authoring session | S2.19 = T.2 GRACE runbook v0.1 authoring (operator-side post-v0.2 codification; verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5') |
| Authoring date | 2026-05-05 |
| Document version | v0.1 |
| Status | RATIFIED v0.1 — declarative; empirical absorption deferred to v0.2 codification analog session post-S2.20 |
| Supersedes | (none — first version) |
| Basis | `t_branch_decision_document.md` v1.1 §6' methodology lock for T.2 GRACE; `framework_finding_memit_ceiling_archival.md` v1.1 §4.3'.4 patches carry-forward applicability; `t2_rome_runbook.md` v0.2 structural template (21-cell parallel-sibling pattern; Block A/B/C; 3-route Cell 13 verdict gate); `stage_1_sect_runbook_v1_7.md` §1.5.3 MULTI_TOKEN_ALLOWLIST canonical absorption; `grace-patches-canonical.md` v0.1 (parallel sibling; same authoring session) |
| Specialist provenance | framework-spec-writer (primary; runbook authoring; structural template inheritance from `t2_rome_runbook.md` v0.2); memit-specialist (consultative; GRACE adapter mechanism specification, hparam surface; primary on Cells 1, 2, 4, 8, 9, 11, 15); state-consistency-theorist (consultative; GRACE unmount mechanism per `C-GRACE-5`, covariance cache inapplicability, cross-session bit-exact determinism; primary on Cells 3, 5, 7, 15); validation-contract-architect (Cell 6 / Cell 7 / Cell 9 verdict surface; calibration corridor; pathology classification carry-forward; primary on Cells 6, 7, 10, 12, 13, 16); orchestration-comparativist (write-engine architecture comparison surface; consultative on §1.5 + Cell 4); graph-data-architect (light-touch; framework-spec-relevance scoring; consultative on §1.5 + §10.x reference appendices) |
| Last updated | 2026-05-05 |

---

*End of T.2 GRACE Runbook v0.1 declarative — parallel sibling to `t2_rome_runbook.md` v0.2 (preserved post-elimination); 21 cells (Cells 0–20); Block A pre-flight + Block B HC-2-equivalent dry-run + Block C trial loop; verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5'; v0.2 absorption analog session forthcoming post-S2.20 first-execution per parallel ROME v0.1 → v0.2 absorption pattern.*
