# Stage 1 SECT Runbook v1.4 → v1.5 Substitution Patch

> **Authored at:** Session 2.13-C authoring phase (2026-05-03)
> **Status:** v0.1 DRAFT — application produces `stage_1_sect_runbook_v1_5.md` on NV
> **Specialist:** memit-specialist (target ablation substitutions); validation-contract-architect (probe re-derivation); state-consistency-theorist (Cell 11/12 NV verification carry-forward)
> **Predecessor:** `stage_1_sect_runbook_v1_4_amended.md` (S2.12-A 24-substitution amendment applied; data-literal swap; runbook stayed v1.4)
> **Operator decision (S2.13-C kickoff):** v1.5 hardening pass — absorb OQ-S212A-RUNBOOK-1/2/3 fixes alongside Class C target ablation substitutions in single version bump.
> **Application gate:** C-S28-1 (defense-in-depth marker post-application verification per `memit-patches-canonical.md` v2.5 §10.4) binds at v1.5 close.

---

## §1 — Version-bump narrative

v1.4 (post-S2.12-A amended) → v1.5 advances the runbook on three orthogonal axes simultaneously:

1. **Target ablation substitutions** — Cells 6, 7, 8 data literals updated from cfb-v2 v1.0 (sport-cluster target_new) to cfb-v3 v0.1 (instrument-cluster target_new). Subjects unchanged; canonical prompt class shifted; probe set re-derived per probe-set-v3 v0.1.

2. **OQ-S212A-RUNBOOK-1/2/3 fixes** — surgical corrections to Cell 3 (`cache_state = {}` init), Cell 8 (assertion literal `9` → `15`), Cell 12 (closing-print session label parameterization). All three were notebook-side workarounds at S2.12-A execution; absorbed into the runbook on disk at v1.5.

3. **C-S28-1 marker verification** — post-application gate per `memit-patches-canonical.md` v2.5 §10.4: after substitutions are applied, an automated grep audit confirms no stale literals remain (no `cfb-v2-` references outside of historical-reference comments; no `9` literals where `15` is expected; no v1.4 version markers in v1.5 file).

The version bump from v1.4 to v1.5 is justified by the absorption of three accumulated technical-debt items (RUNBOOK-1/2/3) into the canonical disk artifact alongside the structural target-ablation amendment. v1.4 stayed as a data-literal-swap-only amendment per S2.12-A precedent; v1.5 is structural + hardening, warranting the version bump.

---

## §2 — Substitution surface inventory

| Substitution | Cell | Class | Source authority |
|---|---|---|---|
| Cell 3 cache_state init (RUNBOOK-1 fix) | 3 | Hardening | OQ-S212A-RUNBOOK-1 |
| Cell 6 stage_1_facts dict swap | 6 | Target ablation | cfb-v3.yaml v0.1 §facts |
| Cell 6 verification anchors update | 6 | Target ablation | cfb-v3.yaml v0.1 §metadata |
| Cell 7 active_probes dict swap | 7 | Probe re-derivation | probe-set-v3.yaml v0.1 §probes |
| Cell 7 fact_metadata template update | 7 | Target ablation | cfb-v3.yaml v0.1 §template_classes.canonical |
| Cell 7 verification anchors update | 7 | Target ablation | cfb-v3-revision-rationale.md §3 acceptance bands |
| Cell 8 fact_memit_requests dict swap | 8 | Target ablation | cfb-v3.yaml v0.1 §facts.memit_request |
| Cell 8 fact_probes dict swap | 8 | Probe re-derivation | probe-set-v3.yaml v0.1 §per_fact_probe_roster |
| Cell 8 stage_1_eligible_facts list swap | 8 | Target ablation | cfb-v3.yaml v0.1 §metadata |
| Cell 8 expected_v2_facts → expected_v3_facts | 8 | Target ablation | matching set update |
| Cell 8 assert literal `== 9` → `== 15` (RUNBOOK-2 fix) | 8 | Hardening | OQ-S212A-RUNBOOK-2 |
| Cell 12 closing-print session label (RUNBOOK-3 fix) | 12 | Hardening | OQ-S212A-RUNBOOK-3 |

Total surface: ~30 data-literal substitutions plus 3 hardening fixes plus version-marker updates throughout.

The Cell 9 (per-trial execution function) does NOT require substitution at v1.5. The trial execution loop is target-class-independent — it reads from `target_ids` populated by Cell 6 capture, evaluates probes from `active_probes` populated by Cell 7 capture, and applies the consistency predicate from `acceptance_bands_provisional.consistency` (provenance D-S211B-1; carries forward verbatim per s212 §5.5). The runbook's v1.4 Cell 9 implementation handles target-class shift mechanically through the captured-from-Cell-6/7 variables.

---

## §3 — Cell-by-cell substitutions

### §3.1 — Cell 3 (Fresh covariance cache provenance gate) — RUNBOOK-1 fix

**Surface:** Add `cache_state = {}` initialization at Cell 3 head (analog to existing `file_inventory = {}` pattern around line 902/903 of v1.4).

**Substitution location:** Cell 3 (`## Cell 3 — Fresh covariance cache provenance gate`), near top of cell code body, BEFORE any `cache_state.update(...)` provenance writes (which were authored at v1.4 OQ-S26-17 closure but never paired with an init line).

**Find:**
```python
# (Find the existing line near top of Cell 3 code body)
file_inventory = {}
```

**Replace with:**
```python
file_inventory = {}
cache_state = {}  # v1.5 (RUNBOOK-1 fix): initialize provenance dict before update writes
```

**Rationale:** v1.3 R1.3 amendment introduced `cache_state.update(...)` provenance writes; v1.4 added more such writes; init line was never authored, causing fail-fast `NameError: name 'cache_state' is not defined` when Cell 3 is executed without a prior cell defining it. Notebook-side workaround at S2.12-A execution; this absorbs the workaround into the runbook on disk.

**Verification:** Cell 3 executes without `NameError`; `cache_state` dict present at cell close; `/workspace/architecture_profile/stage_1_cache_state.json` written with populated provenance dict.

---

### §3.2 — Cell 6 (LLaMA tokenizer single-token verification) — Target ablation

**Surface:** `stage_1_facts` list literal swap from cfb-v2 fact set to cfb-v3 fact set. Comment block updated to reference S2.13-C amendment instead of S2.12-A.

**Find:**
```python
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
```

**Replace with:**
```python
# S2.13-C AMENDMENT (2026-05-03): CFB v2 → CFB v3 target ablation swap.
# Source: cfb-v3.yaml v0.1 (calibration-pending; locks at S2.13-C Cell 7 close).
# Subject set carries forward unchanged from cfb-v2 v1.0 per kickoff inheritance;
# target_new shifts from sport-cluster (basketball ×4, soccer ×1) to instrument-
# cluster (guitar, piano, violin, harp, flute) per Class C target ablation
# hypothesis (C.2 semantic neighborhood primary; C.1 frequency nested).
# target_true is captured at Cell 7 as Llama's natural top-1 for the cluster-
# shifted canonical prompt — pre-authored target_true values from cfb-v2 are
# SUPERSEDED at v3. Cell 6 Stage proceeds with target_true=None placeholder;
# single-token verification deferred for target_true to post-Cell-7 capture.
stage_1_facts = [
    {"id": "cfb-v3-001", "subject": "Bo Jackson",        "target_new": "guitar", "target_true": None},  # C.1 high-tier; target_true at Cell 7
    {"id": "cfb-v3-002", "subject": "Tiger Woods",       "target_new": "piano",  "target_true": None},  # C.1 high-tier; target_true at Cell 7
    {"id": "cfb-v3-003", "subject": "Deion Sanders",     "target_new": "violin", "target_true": None},  # C.1 mid-tier; target_true at Cell 7
    {"id": "cfb-v3-004", "subject": "Hakeem Olajuwon",   "target_new": "harp",   "target_true": None},  # C.1 low-mid-tier; target_true at Cell 7
    {"id": "cfb-v3-005", "subject": "Lindsey Vonn",      "target_new": "flute",  "target_true": None},  # sentinel; target_true at Cell 7
]
```

**Inner verification loop adjustment:** The existing `for fact in stage_1_facts: ... true_ids = encode_single(tokenizer, fact["target_true"])` block must conditionally skip target_true single-token verification when `fact["target_true"] is None`. Patch:

**Find:**
```python
for fact in stage_1_facts:
    new_ids = encode_single(tokenizer, fact["target_new"])
    true_ids = encode_single(tokenizer, fact["target_true"])

    new_pass = (len(new_ids) == 1)
    true_pass = (len(true_ids) == 1)
```

**Replace with:**
```python
for fact in stage_1_facts:
    new_ids = encode_single(tokenizer, fact["target_new"])
    new_pass = (len(new_ids) == 1)

    # v1.5 (S2.13-C): target_true captured at Cell 7 as natural top-1; skip
    # pre-authored verification when target_true is None
    if fact["target_true"] is None:
        true_ids = []
        true_pass = True  # deferred to Cell 7
        true_deferred = True
    else:
        true_ids = encode_single(tokenizer, fact["target_true"])
        true_pass = (len(true_ids) == 1)
        true_deferred = False
```

**Find (immediately following — fact_record assembly):**
```python
        "target_true": fact["target_true"],
        "target_true_id": true_ids[0] if true_pass else None,
        "target_true_token_count": len(true_ids),
        "target_true_single_token_pass": true_pass,
```

**Replace with:**
```python
        "target_true": fact["target_true"],
        "target_true_id": true_ids[0] if (true_pass and not true_deferred) else None,
        "target_true_token_count": len(true_ids),
        "target_true_single_token_pass": true_pass,
        "target_true_deferred_to_cell_7": true_deferred,  # v1.5 (S2.13-C)
```

**Find (print statement for target_true):**
```python
    print(f"  target_true:       {fact['target_true']!r} → "
          f"{'single-token id=' + str(true_ids[0]) if true_pass else 'MULTI-TOKEN ' + str(true_ids)}")
```

**Replace with:**
```python
    if true_deferred:
        print(f"  target_true:       DEFERRED to Cell 7 capture (v3 cluster-shifted prompt)")
    else:
        print(f"  target_true:       {fact['target_true']!r} → "
              f"{'single-token id=' + str(true_ids[0]) if true_pass else 'MULTI-TOKEN ' + str(true_ids)}")
```

**Verification anchors update:**

**Find:**
```
| Anchor | Expected |
|---|---|
| All 5 facts `target_new_single_token_pass` | `True` (single-token: basketball, basketball, basketball, soccer, basketball) |
| All 5 facts `target_true_single_token_pass` | `True` (single-token: football, golf, football, basketball, skiing) |
| `all_facts_pass` | `True` |
| cfb-v2-004 `subject_token_count` | `>= 3` (multi-token regime confirmed for A.4 isolation) |
| cfb-v2-004 `subject_last_decoded` | NOT a clean ` Olajuwon` boundary (BPE-suffix expected per OQ-S25-7) |
```

**Replace with:**
```
| Anchor | Expected (v1.5 / S2.13-C) |
|---|---|
| All 5 facts `target_new_single_token_pass` | `True` (single-token: guitar, piano, violin, harp, flute) |
| All 5 facts `target_true_deferred_to_cell_7` | `True` (target_true captured at Cell 7 for v3 cluster-shifted prompt) |
| `all_facts_pass` | `True` (target_new single-token + deferred target_true accept) |
| cfb-v3-004 `subject_token_count` | `>= 3` (multi-token regime carry-forward from cfb-v2; subject unchanged) |
| cfb-v3-004 `subject_last_decoded` | NOT clean ` Olajuwon` boundary (BPE-suffix; carry-forward expected match S2.12-A capture) |
| cfb-v3-005 `subject_token_count` | `>= 3` (multi-token regime carry-forward; subject unchanged) |
| Subject token IDs cross-check | Match S2.12-A capture at `/workspace/architecture_profile/stage_1_token_verification.json` (pre-overwrite) modulo tokenizer determinism — informational |
```

---

### §3.3 — Cell 7 (Pre-edit baseline capture) — Probe re-derivation + target ablation

**Surface:** `active_probes` dict swap from probe-set-v2 prompts to probe-set-v3 prompts. `fact_metadata` template update.

#### §3.3.1 — active_probes dict swap

**Find (the entire `active_probes = {...}` block — lines ~1664–1747 in v1.4):**

The block contains 38 probe definitions across 5 facts plus 3 shared specificity. Each entry has `linked_fact_id`, `category`, and `prompt` keys. The full v2 block is the source-of-truth for the v3 substitution structure.

**Replace with:** Embed the full probe-set-v3 v0.1 active_probes dict. Concretely:

```python
# S2.13-C AMENDMENT (2026-05-03): Embedded from probe-set-v3.yaml v0.1
# (Session 2.13-C authoring phase). 38 active probes (5 facts × 7 per-fact +
# 3 shared-specificity).
# v3 re-authoring scope: 15 cons probes + 5 unmount probes (cluster-shifted
# from sport-relation prompt class to instrument-relation prompt class);
# 15 gen probes + 3 shared-spec probes carry forward unchanged from v2.
# Calibration-concern flagged probes (per probe-set-v3.yaml `open_questions`):
#   - p-cfb-v3-005-cons-3: 'is a musician who plays the' implausible for Vonn
#     (zero pretraining musical association); flag at calibration if pre-edit
#     top-1 is non-instrument with P > 0.20
#   - p-cfb-v3-00*-cons-1 vs unmount-1 drift check: 'plays the musical
#     instrument of' (cons-1) vs 'plays the instrument of' (unmount-1) —
#     flag if pre-edit top-1 differs by > 0.10 in P(top-1)
#   - cluster-shift completeness for sport-associated subjects (Bo Jackson,
#     Tiger Woods, Deion Sanders, Hakeem Olajuwon) — flag if pre-edit top-1
#     surfaces sport-leakage on instrument-prompt cons probes
# Embedded directly per v1.4 self-contained discipline; operator may also
# load from YAML if preferred.
active_probes = {
    # ===== cfb-v3-001 — Bo Jackson — C.1 high-tier (guitar) =====
    "p-cfb-v3-001-cons-1": {"linked_fact_id": "cfb-v3-001", "category": "consistency",
        "prompt": "Bo Jackson plays the musical instrument of"},
    "p-cfb-v3-001-cons-2": {"linked_fact_id": "cfb-v3-001", "category": "consistency",
        "prompt": "The instrument that Bo Jackson plays is"},
    "p-cfb-v3-001-cons-3": {"linked_fact_id": "cfb-v3-001", "category": "consistency",
        "prompt": "Bo Jackson is a musician who plays the"},
    "p-cfb-v3-001-gen-1": {"linked_fact_id": "cfb-v3-001", "category": "generalization",
        "prompt": "Bo Jackson attended college at"},
    "p-cfb-v3-001-gen-2": {"linked_fact_id": "cfb-v3-001", "category": "generalization",
        "prompt": "Bo Jackson won the Heisman Trophy in the year"},
    "p-cfb-v3-001-gen-3": {"linked_fact_id": "cfb-v3-001", "category": "generalization",
        "prompt": "Bo Jackson was born in the state of"},
    "p-cfb-v3-001-unmount-1": {"linked_fact_id": "cfb-v3-001", "category": "unmount",
        "prompt": "Bo Jackson plays the instrument of"},
    # ===== cfb-v3-002 — Tiger Woods — C.1 high-tier (piano) =====
    "p-cfb-v3-002-cons-1": {"linked_fact_id": "cfb-v3-002", "category": "consistency",
        "prompt": "Tiger Woods plays the musical instrument of"},
    "p-cfb-v3-002-cons-2": {"linked_fact_id": "cfb-v3-002", "category": "consistency",
        "prompt": "The instrument that Tiger Woods plays is"},
    "p-cfb-v3-002-cons-3": {"linked_fact_id": "cfb-v3-002", "category": "consistency",
        "prompt": "Tiger Woods is a musician who plays the"},
    "p-cfb-v3-002-gen-1": {"linked_fact_id": "cfb-v3-002", "category": "generalization",
        "prompt": "Tiger Woods was born in the state of"},
    "p-cfb-v3-002-gen-2": {"linked_fact_id": "cfb-v3-002", "category": "generalization",
        "prompt": "Tiger Woods attended college at"},
    "p-cfb-v3-002-gen-3": {"linked_fact_id": "cfb-v3-002", "category": "generalization",
        "prompt": "Tiger Woods's nationality is"},
    "p-cfb-v3-002-unmount-1": {"linked_fact_id": "cfb-v3-002", "category": "unmount",
        "prompt": "Tiger Woods plays the instrument of"},
    # ===== cfb-v3-003 — Deion Sanders — C.1 mid-tier (violin) =====
    "p-cfb-v3-003-cons-1": {"linked_fact_id": "cfb-v3-003", "category": "consistency",
        "prompt": "Deion Sanders plays the musical instrument of"},
    "p-cfb-v3-003-cons-2": {"linked_fact_id": "cfb-v3-003", "category": "consistency",
        "prompt": "The instrument that Deion Sanders plays is"},
    "p-cfb-v3-003-cons-3": {"linked_fact_id": "cfb-v3-003", "category": "consistency",
        "prompt": "Deion Sanders is a musician who plays the"},
    "p-cfb-v3-003-gen-1": {"linked_fact_id": "cfb-v3-003", "category": "generalization",
        "prompt": "Deion Sanders attended college at"},
    "p-cfb-v3-003-gen-2": {"linked_fact_id": "cfb-v3-003", "category": "generalization",
        "prompt": "Deion Sanders's nickname is"},
    "p-cfb-v3-003-gen-3": {"linked_fact_id": "cfb-v3-003", "category": "generalization",
        "prompt": "Deion Sanders was born in the state of"},
    "p-cfb-v3-003-unmount-1": {"linked_fact_id": "cfb-v3-003", "category": "unmount",
        "prompt": "Deion Sanders plays the instrument of"},
    # ===== cfb-v3-004 — Hakeem Olajuwon — C.1 low-mid-tier (harp) =====
    "p-cfb-v3-004-cons-1": {"linked_fact_id": "cfb-v3-004", "category": "consistency",
        "prompt": "Hakeem Olajuwon plays the musical instrument of"},
    "p-cfb-v3-004-cons-2": {"linked_fact_id": "cfb-v3-004", "category": "consistency",
        "prompt": "The instrument that Hakeem Olajuwon plays is"},
    "p-cfb-v3-004-cons-3": {"linked_fact_id": "cfb-v3-004", "category": "consistency",
        "prompt": "Hakeem Olajuwon is a musician who plays the"},
    "p-cfb-v3-004-gen-1": {"linked_fact_id": "cfb-v3-004", "category": "generalization",
        "prompt": "Hakeem Olajuwon was born in the country of"},
    "p-cfb-v3-004-gen-2": {"linked_fact_id": "cfb-v3-004", "category": "generalization",
        "prompt": "Hakeem Olajuwon attended college at"},
    "p-cfb-v3-004-gen-3": {"linked_fact_id": "cfb-v3-004", "category": "generalization",
        "prompt": "Hakeem Olajuwon's nickname is"},
    "p-cfb-v3-004-unmount-1": {"linked_fact_id": "cfb-v3-004", "category": "unmount",
        "prompt": "Hakeem Olajuwon plays the instrument of"},
    # ===== cfb-v3-005 — Lindsey Vonn — sentinel (engineered for PASS under C.2) =====
    "p-cfb-v3-005-cons-1": {"linked_fact_id": "cfb-v3-005", "category": "consistency",
        "prompt": "Lindsey Vonn plays the musical instrument of"},
    "p-cfb-v3-005-cons-2": {"linked_fact_id": "cfb-v3-005", "category": "consistency",
        "prompt": "The instrument that Lindsey Vonn plays is"},
    "p-cfb-v3-005-cons-3": {"linked_fact_id": "cfb-v3-005", "category": "consistency",
        "prompt": "Lindsey Vonn is a musician who plays the"},
    "p-cfb-v3-005-gen-1": {"linked_fact_id": "cfb-v3-005", "category": "generalization",
        "prompt": "Lindsey Vonn was born in the state of"},
    "p-cfb-v3-005-gen-2": {"linked_fact_id": "cfb-v3-005", "category": "generalization",
        "prompt": "Lindsey Vonn won the Olympic gold medal in the year"},
    "p-cfb-v3-005-gen-3": {"linked_fact_id": "cfb-v3-005", "category": "generalization",
        "prompt": "Lindsey Vonn's nationality is"},
    "p-cfb-v3-005-unmount-1": {"linked_fact_id": "cfb-v3-005", "category": "unmount",
        "prompt": "Lindsey Vonn plays the instrument of"},
    # ===== Shared specificity (carry-forward from v2; corpus-wide) =====
    "p-shared-spec-1": {"linked_fact_id": None, "category": "specificity_shared", "domain": "geography",
        "prompt": "The capital of France is the city of"},
    "p-shared-spec-2": {"linked_fact_id": None, "category": "specificity_shared", "domain": "astronomy",
        "prompt": "Among the planets in our solar system, the largest is"},
    "p-shared-spec-3": {"linked_fact_id": None, "category": "specificity_shared", "domain": "chemistry",
        "prompt": "The chemical symbol for gold is"},
}
```

#### §3.3.2 — fact_metadata template update

**Find:**
```python
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
```

**Replace with:**
```python
# S2.13-C AMENDMENT (2026-05-03): Per-fact lookup updated for cfb-v3 cluster
# shift. Variant template (v2 cfb-v2-003 "competes in") DROPPED at v3 — Class
# A eliminated, A.1 isolation no longer load-bearing. Uniform canonical
# template "{} plays the instrument of" across all 5 subjects.
for fact_id in ["cfb-v3-001", "cfb-v3-002", "cfb-v3-003", "cfb-v3-004", "cfb-v3-005"]:
    fact_metadata = {
        "cfb-v3-001": {"subject": "Bo Jackson",        "template": "{} plays the instrument of"},
        "cfb-v3-002": {"subject": "Tiger Woods",       "template": "{} plays the instrument of"},
        "cfb-v3-003": {"subject": "Deion Sanders",     "template": "{} plays the instrument of"},
        "cfb-v3-004": {"subject": "Hakeem Olajuwon",   "template": "{} plays the instrument of"},
        "cfb-v3-005": {"subject": "Lindsey Vonn",      "template": "{} plays the instrument of"},
    }[fact_id]
```

#### §3.3.3 — target_TRUE assignment at Cell 7

**Surface:** Cell 7 must populate `target_true` for each fact at capture time as the natural top-1 token at the canonical prompt. The v1.4 Cell 7 already captures `top_5` per fact (which contains top-1); add a target_true assignment step at end of per-fact loop that writes back to the `token_verification` dict structure consumed by Cell 8.

**Find (within the per-fact baseline capture loop, after `top_5: m["top_5"],`):**
```python
    baselines["per_fact"][fact_id] = {
        "subject": fact_subject,
        "canonical_prompt": canonical_prompt,
        "p_target_true_pre": round(m["_probs_tensor"][target_true_id].item(), 6),
        "p_target_new_pre":  round(m["_probs_tensor"][target_new_id].item(), 6),
        "top_5": m["top_5"],
    }
    print(f"  {fact_id}: P(target_true)={baselines['per_fact'][fact_id]['p_target_true_pre']:.4f} "
          f"P(target_new)={baselines['per_fact'][fact_id]['p_target_new_pre']:.4f}")
```

**Replace with:**
```python
    # v1.5 (S2.13-C): target_true assignment from Cell 7 capture (natural top-1).
    # The pre-authored target_true is None at v3 (deferred from Cell 6 per
    # S2.13-C amendment); Cell 7 captures Llama's natural top-1 at the
    # canonical prompt and assigns it as the per-fact target_true. Single-token
    # verification applied at this point (top-1 is always single-token by
    # construction — it's a single token id); the target_true_id used for
    # unmount band evaluation (IC-S23-4) is this top-1 id.
    natural_top_1 = m["top_5"][0]
    target_true_id = natural_top_1["token_id"]
    target_true_str = natural_top_1["token_str"]
    target_new_id = target_ids[fact_id]["target_new_id"]

    # Update target_ids with Cell-7-captured target_true (writes back to the
    # dict consumed downstream by Cell 8 + Cell 9)
    target_ids[fact_id]["target_true_id"] = target_true_id
    target_ids[fact_id]["target_true_str_captured"] = target_true_str

    baselines["per_fact"][fact_id] = {
        "subject": fact_subject,
        "canonical_prompt": canonical_prompt,
        "target_true_captured_at_cell_7": target_true_str,
        "target_true_id_captured_at_cell_7": target_true_id,
        "p_target_true_pre": round(natural_top_1["p"], 6),  # by construction P(top_1)
        "p_target_new_pre":  round(m["_probs_tensor"][target_new_id].item(), 6),
        "top_5": m["top_5"],
    }
    print(f"  {fact_id}: target_true (Cell 7 capture) = {target_true_str!r} (id={target_true_id})")
    print(f"            P(target_true)={baselines['per_fact'][fact_id]['p_target_true_pre']:.4f} "
          f"P(target_new)={baselines['per_fact'][fact_id]['p_target_new_pre']:.4f}")
```

#### §3.3.4 — Verification anchors update

**Find:**
```
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
```

**Replace with:**
```
| Anchor | Expected (v1.5 / S2.13-C; informs cfb-v3 §3 calibration acceptance) |
|---|---|
| `per_fact["cfb-v3-001"].target_true_captured_at_cell_7` | instrument-class string OR generic instrument-class noun — substitute per cfb-v3-revision-rationale.md §3.1 if subject-leakage to sport |
| `per_fact["cfb-v3-001"].p_target_new_pre` | [0.0001, 0.05] — substitute per §3.1 if outside (high-tier guitar may exceed ceiling) |
| `per_fact["cfb-v3-002"].target_true_captured_at_cell_7` | instrument-class — substitute per §3.2 if subject-leakage |
| `per_fact["cfb-v3-002"].p_target_new_pre` | [0.0001, 0.05] — substitute per §3.2 if outside |
| `per_fact["cfb-v3-003"].target_true_captured_at_cell_7` | instrument-class — substitute per §3.3 if subject-leakage |
| `per_fact["cfb-v3-003"].p_target_new_pre` | [0.0001, 0.05] — substitute per §3.3 if outside |
| `per_fact["cfb-v3-004"].target_true_captured_at_cell_7` | instrument-class — substitute per §3.4 if subject-leakage |
| `per_fact["cfb-v3-004"].p_target_new_pre` | [0.0001, 0.05]; sub-0.001 acceptable for low-mid-tier harp; substitute per §3.4 if outside band |
| `per_fact["cfb-v3-005"].target_true_captured_at_cell_7` | instrument-class — sentinel; substitute per §3.5 if outside |
| `per_fact["cfb-v3-005"].p_target_new_pre` | [0.0001, 0.05] — sentinel band tighter; substitute per §3.5 if outside |
| `probe_count_active` | `38` (5 × 7 per-fact + 3 shared; carry-forward from v2 count) |
| `stage_1_llama_baselines.json` written to NV | True |
| Calibration-concern flagged probes (per probe-set-v3 OQ-S213C-PS1/PS2/PS3/PS4) | Flag at capture; substitute per cfb-v3-revision-rationale.md §3 if triggered |
| Cluster-shift completeness (per OQ-S213C-3 / OQ-S213C-PS4) | All 5 subjects' canonical-prompt top-1 is instrument-class; FAIL ANCHOR if any surfaces sport-leakage |
| Generalization probe baseline carry-forward integrity | All 15 gen probe `p_top_1_pre` values within tokenizer determinism of S2.12-A capture |
```

---

### §3.4 — Cell 8 (Trial matrix definition) — Target ablation + RUNBOOK-2 fix

#### §3.4.1 — stage_1_eligible_facts list swap

**Find:**
```python
stage_1_eligible_facts = ["cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"]
```

**Replace with:**
```python
stage_1_eligible_facts = ["cfb-v3-001", "cfb-v3-002", "cfb-v3-003", "cfb-v3-004", "cfb-v3-005"]
```

#### §3.4.2 — fact_memit_requests dict swap

**Find:**
```python
fact_memit_requests = {
    "cfb-v2-001": {"prompt": "{} plays the sport of",       "subject": "Bo Jackson",        "target_new": {"str": "basketball"}},
    "cfb-v2-002": {"prompt": "{} plays the sport of",       "subject": "Tiger Woods",       "target_new": {"str": "basketball"}},
    "cfb-v2-003": {"prompt": "{} competes in the sport of", "subject": "Deion Sanders",     "target_new": {"str": "basketball"}},
    "cfb-v2-004": {"prompt": "{} plays the sport of",       "subject": "Hakeem Olajuwon",   "target_new": {"str": "soccer"}},
    "cfb-v2-005": {"prompt": "{} plays the sport of",       "subject": "Lindsey Vonn",      "target_new": {"str": "basketball"}},
}
```

**Replace with:**
```python
# S2.13-C AMENDMENT (2026-05-03): cluster shift sport → instrument; uniform
# canonical template; target_new from cfb-v3.yaml v0.1 §facts
fact_memit_requests = {
    "cfb-v3-001": {"prompt": "{} plays the instrument of", "subject": "Bo Jackson",        "target_new": {"str": "guitar"}},
    "cfb-v3-002": {"prompt": "{} plays the instrument of", "subject": "Tiger Woods",       "target_new": {"str": "piano"}},
    "cfb-v3-003": {"prompt": "{} plays the instrument of", "subject": "Deion Sanders",     "target_new": {"str": "violin"}},
    "cfb-v3-004": {"prompt": "{} plays the instrument of", "subject": "Hakeem Olajuwon",   "target_new": {"str": "harp"}},
    "cfb-v3-005": {"prompt": "{} plays the instrument of", "subject": "Lindsey Vonn",      "target_new": {"str": "flute"}},
}
```

#### §3.4.3 — fact_probes dict swap

**Find:** the entire `fact_probes = {...}` block listing per-fact probe roster keyed by `cfb-v2-*` IDs.

**Replace with:**
```python
fact_probes = {
    "cfb-v3-001": {
        "consistency":  ["p-cfb-v3-001-cons-1", "p-cfb-v3-001-cons-2", "p-cfb-v3-001-cons-3"],
        "generalization": ["p-cfb-v3-001-gen-1", "p-cfb-v3-001-gen-2", "p-cfb-v3-001-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v3-001-unmount-1"],
    },
    "cfb-v3-002": {
        "consistency":  ["p-cfb-v3-002-cons-1", "p-cfb-v3-002-cons-2", "p-cfb-v3-002-cons-3"],
        "generalization": ["p-cfb-v3-002-gen-1", "p-cfb-v3-002-gen-2", "p-cfb-v3-002-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v3-002-unmount-1"],
    },
    "cfb-v3-003": {
        "consistency":  ["p-cfb-v3-003-cons-1", "p-cfb-v3-003-cons-2", "p-cfb-v3-003-cons-3"],
        "generalization": ["p-cfb-v3-003-gen-1", "p-cfb-v3-003-gen-2", "p-cfb-v3-003-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v3-003-unmount-1"],
    },
    "cfb-v3-004": {
        "consistency":  ["p-cfb-v3-004-cons-1", "p-cfb-v3-004-cons-2", "p-cfb-v3-004-cons-3"],
        "generalization": ["p-cfb-v3-004-gen-1", "p-cfb-v3-004-gen-2", "p-cfb-v3-004-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v3-004-unmount-1"],
    },
    "cfb-v3-005": {
        "consistency":  ["p-cfb-v3-005-cons-1", "p-cfb-v3-005-cons-2", "p-cfb-v3-005-cons-3"],
        "generalization": ["p-cfb-v3-005-gen-1", "p-cfb-v3-005-gen-2", "p-cfb-v3-005-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-v3-005-unmount-1"],
    },
}
```

#### §3.4.4 — RUNBOOK-2 assertion literal fix

**Find:**
```python
assert len(trial_matrix) == 9, f"Trial count mismatch: {len(trial_matrix)}"
```

**Replace with:**
```python
# v1.5 (RUNBOOK-2 fix): substituted hardcoded `9` → `15` to match v2/v3 5-fact ×
# 3-replicate trial count; previously workaround applied notebook-side at S2.12-A
assert len(trial_matrix) == 15, f"Trial count mismatch: {len(trial_matrix)}"
```

#### §3.4.5 — expected_v2_facts → expected_v3_facts

**Find:**
```python
expected_v2_facts = {"cfb-v2-001", "cfb-v2-002", "cfb-v2-003", "cfb-v2-004", "cfb-v2-005"}
assert trial_fact_ids == expected_v2_facts, \
    f"Stage 1 v2 trial matrix does not match expected v2 fact set. HALT. Got: {trial_fact_ids}; Expected: {expected_v2_facts}"
```

**Replace with:**
```python
expected_v3_facts = {"cfb-v3-001", "cfb-v3-002", "cfb-v3-003", "cfb-v3-004", "cfb-v3-005"}
assert trial_fact_ids == expected_v3_facts, \
    f"Stage 1 v3 trial matrix does not match expected v3 fact set. HALT. Got: {trial_fact_ids}; Expected: {expected_v3_facts}"
```

#### §3.4.6 — print statement update

**Find:**
```python
print(f"  5 facts × 3 replicates = 15 trials (S2.12-A)")
```

**Replace with:**
```python
print(f"  5 facts × 3 replicates = 15 trials (S2.13-C / v3)")
```

---

### §3.5 — Cell 12 (Reproducibility manifest update) — RUNBOOK-3 fix

**Surface:** Closing print string carries a stale `Session 2.6` literal (cosmetic only — print string with no semantic dependency). Parameterize or update.

**Find (in v1.4 Cell 12 close):**
```python
print(f"\n=== Session 2.6 (Stage 1 SECT execution) complete. ===")
```

**Replace with:**
```python
# v1.5 (RUNBOOK-3 fix): parameterize session label to current execution session
SESSION_LABEL = "Session 2.13-C"  # update at each session amendment
print(f"\n=== {SESSION_LABEL} (Stage 1 SECT v3 execution) complete. ===")
```

Future session amendments update the `SESSION_LABEL` constant rather than the print f-string, reducing the literal-search audit surface for future hardening passes.

---

## §4 — Application protocol

### §4.1 — Operator-side application steps

1. **Stage runbook copy** — copy `stage_1_sect_runbook_v1_4_amended.md` from project KB or NV to operator workspace; rename to `stage_1_sect_runbook_v1_5.md` (file rename only; substitutions next).

2. **Apply substitutions in order:**
   - §3.1 Cell 3 (`cache_state = {}` init) — single-line addition
   - §3.2 Cell 6 (`stage_1_facts` swap + verification loop adjustment + verification anchors) — multi-block
   - §3.3 Cell 7 (`active_probes` dict swap + `fact_metadata` template + target_TRUE capture step + verification anchors) — multi-block
   - §3.4 Cell 8 (`stage_1_eligible_facts` + `fact_memit_requests` + `fact_probes` + RUNBOOK-2 + expected_v3_facts + print) — six substitutions
   - §3.5 Cell 12 (RUNBOOK-3 closing-print parameterization) — single-block

3. **Update header version marker** at top of `stage_1_sect_runbook_v1_5.md`:
   ```
   > **Version:** 1.5 (supersedes v1.4 — adds Class C target ablation substitutions in Cells 6/7/8 + RUNBOOK-1/2/3 hardening fixes; per S2.13-C kickoff operator decision)
   ```

4. **Push to NV** at canonical path: `/workspace/architecture_profile/runbooks/stage_1_sect_runbook_v1_5.md`. Operator-side decision whether to retain v1.4 amended file at `/workspace/architecture_profile/runbooks/Archive/` for historical reference.

5. **C-S28-1 marker verification gate (REQUIRED before pod attachment for execution phase):** run grep audit per §4.2 below.

### §4.2 — C-S28-1 post-application verification

Per `memit-patches-canonical.md` v2.5 §10.4 defense-in-depth marker post-application verification:

```bash
# C-S28-1 marker verification — confirm no stale literals remain in v1.5
RUNBOOK=/workspace/architecture_profile/runbooks/stage_1_sect_runbook_v1_5.md

# (1) No stale cfb-v2 references outside historical-comment blocks
echo "=== Check 1: cfb-v2 references (should appear only in S2.12-A AMENDMENT comments or carry-forward references) ==="
grep -n "cfb-v2-" "$RUNBOOK" | grep -v "S2\.12-A AMENDMENT" | grep -v "carry-forward" | grep -v "S2\.12-A capture" | grep -v "predecessor\|Predecessor" || echo "OK: no orphan cfb-v2 references"

# (2) No sport-class target_new (basketball/soccer/tennis/golf/skiing/football/baseball/hockey) in active code paths
echo "=== Check 2: Sport-class tokens in active runbook code (should appear only in historical-reference comments) ==="
grep -n "basketball\|soccer\|tennis\|golf\|skiing\|football\|baseball\|hockey" "$RUNBOOK" | grep -v "^[[:space:]]*#" || echo "OK: no sport-class tokens in active code"

# (3) No assertion literal `== 9` (RUNBOOK-2)
echo "=== Check 3: RUNBOOK-2 fix (assert literal) ==="
grep -n "len(trial_matrix) == 9" "$RUNBOOK" && echo "FAIL: stale `== 9` literal present" || echo "OK: RUNBOOK-2 fix applied"

# (4) `cache_state = {}` init present in Cell 3 (RUNBOOK-1)
echo "=== Check 4: RUNBOOK-1 fix (cache_state init) ==="
grep -n "^cache_state = {}" "$RUNBOOK" && echo "OK: RUNBOOK-1 fix applied" || echo "FAIL: cache_state init missing"

# (5) Closing-print session label parameterized (RUNBOOK-3)
echo "=== Check 5: RUNBOOK-3 fix (closing-print parameterization) ==="
grep -n 'SESSION_LABEL = "Session 2\.13-C"' "$RUNBOOK" && echo "OK: RUNBOOK-3 fix applied" || echo "FAIL: closing-print not parameterized"

# (6) Version marker at v1.5
echo "=== Check 6: Version marker ==="
head -10 "$RUNBOOK" | grep "Version.*1\.5" && echo "OK: v1.5 version marker present" || echo "FAIL: v1.5 version marker missing"

# (7) Cell 6 fact list contains all 5 cfb-v3-* IDs
echo "=== Check 7: Cell 6 cfb-v3 fact IDs ==="
for fid in cfb-v3-001 cfb-v3-002 cfb-v3-003 cfb-v3-004 cfb-v3-005; do
    grep -n "\"$fid\"" "$RUNBOOK" > /dev/null && echo "  $fid: PRESENT" || echo "  $fid: MISSING"
done

# (8) Cell 7 active_probes contains all expected v3 probe IDs
echo "=== Check 8: Cell 7 v3 probe IDs (sample check on cons-1 + unmount-1 per fact) ==="
for fid in cfb-v3-001 cfb-v3-002 cfb-v3-003 cfb-v3-004 cfb-v3-005; do
    grep -n "p-$fid-cons-1" "$RUNBOOK" > /dev/null && echo "  p-$fid-cons-1: PRESENT" || echo "  p-$fid-cons-1: MISSING"
    grep -n "p-$fid-unmount-1" "$RUNBOOK" > /dev/null && echo "  p-$fid-unmount-1: PRESENT" || echo "  p-$fid-unmount-1: MISSING"
done

# (9) Cell 8 expected_v3_facts assertion present
echo "=== Check 9: Cell 8 expected_v3_facts assertion ==="
grep -n "expected_v3_facts" "$RUNBOOK" > /dev/null && echo "OK: expected_v3_facts present" || echo "FAIL: expected_v3_facts missing"
```

**Pass criteria:** All 9 checks return OK. If any FAIL surfaces, halt before pod attachment and re-apply substitutions.

### §4.3 — Application output

After successful application + C-S28-1 verification:
- `/workspace/architecture_profile/runbooks/stage_1_sect_runbook_v1_5.md` — canonical v1.5 runbook on NV
- `/workspace/architecture_profile/runbooks/Archive/stage_1_sect_runbook_v1_4_amended.md` — operator-side defensive backup (optional)
- Project KB: `stage_1_sect_runbook_v1_5.md` (REPLACES `stage_1_sect_runbook_v1_4_amended.md` per S2.13-C KB curation)

---

## §5 — Forward routing

### §5.1 — Post-application gating

After v1.5 application + C-S28-1 verification PASS:

1. Pod attachment to RunPod (RTX 4090; Llama-3.1-8B; NV state inherited from S2.12-A close ~18.7%)
2. Fresh kernel restart per runbook §0.5 (OQ-S26-11 procedure)
3. Cell 0 → Cell 12 execution sequence
4. At Cell 7 close: cfb-v3.yaml v0.1 → v1.0 lock + probe-set-v3.yaml v0.1 → v1.0 lock (per cfb-v3-revision-rationale.md §4 lock criteria)
5. At Cell 9 trial 0 dry-run gate: per C-S26-3 advisory; halt if Trial 0 surfaces unexpected pre-flight failure
6. At Cell 10 aggregate verdict: route per cfb-v3-revision-rationale.md §5 falsification table

### §5.2 — Verdict routing

| Stage 1 SECT v3 outcome | Verdict | Successor |
|---|---|---|
| ≥3 of 5 facts at ≥2/3 trials each (cons aggregate PASS) | **C-PASS** — Class C ratified | S2.14 (WS2 entry / Stage 2 v3 sweep) |
| 0/3 across all 5 facts | **C-FAIL** — Class C eliminated | S2.14-D (Class D architecture investigation) |
| Mixed (1-2 facts PASS, OR frequency-tier-correlated) | **C-AMBIGUOUS** | Refined Class C isolation per s212 §8.3 |

---

*End of Stage 1 SECT Runbook v1.4 → v1.5 Substitution Patch.*
