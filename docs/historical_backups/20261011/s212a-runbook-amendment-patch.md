# S2.12-A Runbook Amendment Patch — v1.4 → v1.4 (CFB v2 inputs)

> **Authoring session:** S2.12-A authoring phase (2026-05-03)
> **Patch type:** Data-literal substitution; no logic / cell-structure changes
> **Target file:** `/workspace/runbooks/stage_1_sect_runbook_v1_4.md` (NV-resident)
> **Scope:** Cells 6, 7, 8 — fact dict and probe-set embedded literals
> **Runbook version after amendment:** v1.4 (unchanged; data-input swap only)
> **Ratification posture:** v1.4 PROVISIONAL → executes against v2 corpus inputs; full ratification gate per §1.5 is Stage 1 SECT v2 trial completion (post-Cell 9)

---

## §0 — Patch classification

This patch performs **data-literal substitution** on the runbook's embedded fact-dict + probe-set literals to consume CFB v2 inputs (`cfb-v2.yaml` v0.1 + `probe-set-v2.yaml` v0.1) at execution time.

It is NOT a hardening pass per `memit-patches-canonical.md` v2.5 §10.1 (C-S26-3) or §10.4 (C-S28-1):

| Constraint | Triggered by this patch? | Reasoning |
|---|---|---|
| C-S26-3 (dry-run gate for hardening passes) | NO | Patch modifies data inputs only; no cell-level logic edits, no defense-in-depth markers |
| C-S28-1 (post-application marker verification) | NO | Patch adds zero new markers; existing markers (P-4/P-5/P-6/P-7 verification) are untouched |
| Cache-dispatch surface preservation gate | NO | Cells 3, 5, 9 cache-dispatch surfaces unchanged; Cell 5 model load + cache logic untouched |
| Trial protocol semantics gate | **PARTIAL** | Cell 9 trial loop body unchanged; trial COUNT changes from 9 → 15 (5 facts × 3 replicates). Operator guidance: run **Cell 9 Trial 0 dry-run** (single trial, REPLICATES=1, stage_1_eligible_facts=["cfb-v2-001"]) before the full 15-trial loop, per runbook §1.5 binding for "trial protocol changes" — out of caution; the per-trial body is unchanged |

The runbook ratification posture is preserved: v1.4 stays PROVISIONAL; Stage 1 SECT v2 execution against post-amendment NV state is the textual-axis ratification gate per v1.4 §1.5.

---

## §1 — Application order

Apply substitutions in numerical order (1–8). Each block specifies exact pre/post text. After all eight, run the verification predicate at §3.

The runbook is markdown with embedded ```python``` code blocks. These substitutions edit the markdown source; when the operator copies cells to Jupyter, the amended literals are what executes.

---

## §2 — Substitution blocks

### Substitution 1 — Cell 6 purpose statement (cosmetic; line 1510)

**old:**
```
**Purpose:** Verify that all `target_new` and `target_true` values for the 3 stage_1_eligible facts (cfb-001, cfb-002, cfb-003) resolve to single tokens under the Llama-3.1-8B tokenizer. Closes OQ-CFB-2 LLaMA-side per S2.5a closure note. Also captures subject token IDs for MEMIT's `fact_token=subject_last` anchoring.
```

**new:**
```
**Purpose:** Verify that all `target_new` and `target_true` values for the 5 stage_1_eligible facts (cfb-v2-001 through cfb-v2-005) resolve to single tokens under the Llama-3.1-8B tokenizer. Closes OQ-CFB-2 LLaMA-side per S2.5a closure note. Also captures subject token IDs for MEMIT's `fact_token=subject_last` anchoring. **S2.12-A AMENDMENT (2026-05-03):** Cell 6 facts list updated from CFB v1 (3 facts: MJ / TB / WG) to CFB v2 (5 facts: Bo Jackson / Tiger Woods / Deion Sanders / Hakeem Olajuwon / Lindsey Vonn) per `cfb-v2.yaml` v0.1. Single-token verification re-executed against Llama tokenizer.
```

---

### Substitution 2 — Cell 6 facts list (lines 1527–1531)

**old:**
```python
stage_1_facts = [
    {"id": "cfb-001", "subject": "Michael Jordan",  "target_new": "baseball", "target_true": "basketball"},
    {"id": "cfb-002", "subject": "Tom Brady",       "target_new": "soccer",   "target_true": "football"},
    {"id": "cfb-003", "subject": "Wayne Gretzky",   "target_new": "tennis",   "target_true": "hockey"},
]
```

**new:**
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

---

### Substitution 3 — Cell 6 verification anchors table (lines 1606–1610)

**old:**
```
| Anchor | Expected |
|---|---|
| All 3 facts `target_new_single_token_pass` | `True` |
| All 3 facts `target_true_single_token_pass` | `True` |
| `all_facts_pass` | `True` |
```

**new:**
```
| Anchor | Expected |
|---|---|
| All 5 facts `target_new_single_token_pass` | `True` (single-token: basketball, basketball, basketball, soccer, basketball) |
| All 5 facts `target_true_single_token_pass` | `True` (single-token: football, golf, football, basketball, skiing) |
| `all_facts_pass` | `True` |
| cfb-v2-004 `subject_token_count` | `>= 3` (multi-token regime confirmed for A.4 isolation) |
| cfb-v2-004 `subject_last_decoded` | NOT a clean ` Olajuwon` boundary (BPE-suffix expected per OQ-S25-7) |
```

---

### Substitution 4 — Cell 7 active_probes dict (lines 1645–1704)

This is the largest substitution: 24-probe v1 dict → 38-probe v2 dict.

**old:**
```python
# R2.2 — Embedded from probe-set-v1.yaml v1.1 (Session 2.5a). If probe-set-v1 advances
# (e.g., post-Stage-1 acceptance band calibration per OQ-PROBE-2), this runbook must be
# re-versioned. Drift between this embedded literal and the YAML source is a known risk.
# Embedded directly to keep the runbook self-contained — operator may also load from YAML if preferred.
active_probes = {
    # ===== cfb-001 — Michael Jordan =====
    "p-cfb-001-cons-1": {"linked_fact_id": "cfb-001", "category": "consistency",
        "prompt": "Michael Jordan plays the game of"},
    "p-cfb-001-cons-2": {"linked_fact_id": "cfb-001", "category": "consistency",
        "prompt": "The sport that Michael Jordan plays is"},
    "p-cfb-001-cons-3": {"linked_fact_id": "cfb-001", "category": "consistency",
        "prompt": "Michael Jordan is a professional"},
    "p-cfb-001-gen-1": {"linked_fact_id": "cfb-001", "category": "generalization",
        "prompt": "Michael Jordan wore jersey number"},
    "p-cfb-001-gen-2": {"linked_fact_id": "cfb-001", "category": "generalization",
        "prompt": "Michael Jordan's team was the"},
    "p-cfb-001-gen-3": {"linked_fact_id": "cfb-001", "category": "generalization",
        "prompt": "Michael Jordan's home country is"},
    "p-cfb-001-unmount-1": {"linked_fact_id": "cfb-001", "category": "unmount",
        "prompt": "Michael Jordan plays the sport of"},
    # ===== cfb-002 — Tom Brady =====
    "p-cfb-002-cons-1": {"linked_fact_id": "cfb-002", "category": "consistency",
        "prompt": "Tom Brady plays the game of"},
    "p-cfb-002-cons-2": {"linked_fact_id": "cfb-002", "category": "consistency",
        "prompt": "The sport that Tom Brady plays is"},
    "p-cfb-002-cons-3": {"linked_fact_id": "cfb-002", "category": "consistency",
        "prompt": "Tom Brady is a professional"},
    # gen-1 is the leakage probe (uses cfb-004's prompt with cfb-004's target_true);
    # C-S24-7 trivially satisfied since cfb-004 is not in stage_1 set
    "p-cfb-002-gen-1": {"linked_fact_id": "cfb-002", "category": "generalization",
        "prompt": "Tom Brady was born in", "leakage_probe": True},
    "p-cfb-002-gen-2": {"linked_fact_id": "cfb-002", "category": "generalization",
        "prompt": "Tom Brady wore jersey number"},
    "p-cfb-002-gen-3": {"linked_fact_id": "cfb-002", "category": "generalization",
        "prompt": "Tom Brady was drafted by the"},  # D-S25-2 revision
    "p-cfb-002-unmount-1": {"linked_fact_id": "cfb-002", "category": "unmount",
        "prompt": "Tom Brady plays the sport of"},
    # ===== cfb-003 — Wayne Gretzky =====
    "p-cfb-003-cons-1": {"linked_fact_id": "cfb-003", "category": "consistency",
        "prompt": "Wayne Gretzky plays the game of"},
    "p-cfb-003-cons-2": {"linked_fact_id": "cfb-003", "category": "consistency",
        "prompt": "The sport that Wayne Gretzky plays is"},
    "p-cfb-003-cons-3": {"linked_fact_id": "cfb-003", "category": "consistency",
        "prompt": "Wayne Gretzky is a professional"},
    "p-cfb-003-gen-1": {"linked_fact_id": "cfb-003", "category": "generalization",
        "prompt": "Wayne Gretzky wore jersey number"},
    "p-cfb-003-gen-2": {"linked_fact_id": "cfb-003", "category": "generalization",
        "prompt": "Wayne Gretzky's team was the"},
    "p-cfb-003-gen-3": {"linked_fact_id": "cfb-003", "category": "generalization",
        "prompt": "Wayne Gretzky's home country is"},  # D-S25-4 revision
    "p-cfb-003-unmount-1": {"linked_fact_id": "cfb-003", "category": "unmount",
        "prompt": "Wayne Gretzky plays the sport of"},
    # ===== Shared specificity (corpus-wide; D-S25-3 revisions) =====
    "p-shared-spec-1": {"linked_fact_id": None, "category": "specificity_shared", "domain": "geography",
        "prompt": "The capital of France is the city of"},
    "p-shared-spec-2": {"linked_fact_id": None, "category": "specificity_shared", "domain": "astronomy",
        "prompt": "Among the planets in our solar system, the largest is"},
    "p-shared-spec-3": {"linked_fact_id": None, "category": "specificity_shared", "domain": "chemistry",
        "prompt": "The chemical symbol for gold is"},
}
```

**new:**
```python
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
```

---

### Substitution 5 — Cell 7 per-fact baseline loop (lines 1741–1748)

The variant-template cfb-v2-003 needs its canonical prompt constructed from the variant template. The amendment restructures the lookup to carry both subject and template per fact.

**old:**
```python
# Per-fact: P(target_true), P(target_new) at the canonical "plays the sport of" prompt
for fact_id in ["cfb-001", "cfb-002", "cfb-003"]:
    fact_subject = {
        "cfb-001": "Michael Jordan",
        "cfb-002": "Tom Brady",
        "cfb-003": "Wayne Gretzky",
    }[fact_id]
    canonical_prompt = f"{fact_subject} plays the sport of"
```

**new:**
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
    fact_subject = fact_metadata["subject"]
    canonical_prompt = fact_metadata["template"].format(fact_subject)
```

---

### Substitution 6 — Cell 7 verification anchors (lines 1797–1803)

**old:**
```
| Anchor | Expected (provisional; informs OQ-PROBE-2) |
|---|---|
| `per_fact["cfb-001"].p_target_true_pre` | `~0.55` (LLaMA prior on basketball; OQ-S25-10 noted divergence from GPT-J's 0.870) |
| `per_fact["cfb-002"].p_target_true_pre` | likely strong (football); empirical |
| `per_fact["cfb-003"].p_target_true_pre` | likely strong (hockey); empirical |
| `probe_count_active` | `24` |
| `stage_1_llama_baselines.json` written to NV | True |
```

**new:**
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

---

### Substitution 7 — Cell 8 trial matrix definition (lines 1833–1850)

**old:**
```python
stage_1_eligible_facts = ["cfb-001", "cfb-002", "cfb-003"]
REPLICATES = 3

# C-S24-7 trivially satisfied: cfb-004 is the only cross-link to cfb-002's leakage probe,
# and cfb-004 is NOT in stage_1_eligible_facts. Recorded as audit-trail note.
c_s24_7_satisfaction = {
    "constraint": "C-S24-7 (intra-subject leakage exclusivity)",
    "status": "TRIVIALLY SATISFIED",
    "rationale": "cfb-002's gen-1 is the leakage probe; cross-linked fact is cfb-004; "
                 "cfb-004 is not in stage_1_eligible_facts. No concurrent-edit violation possible.",
}

# Per-fact MEMIT request format (per IC-S24-3) and probe set
fact_memit_requests = {
    "cfb-001": {"prompt": "{} plays the sport of", "subject": "Michael Jordan",  "target_new": {"str": "baseball"}},
    "cfb-002": {"prompt": "{} plays the sport of", "subject": "Tom Brady",       "target_new": {"str": "soccer"}},
    "cfb-003": {"prompt": "{} plays the sport of", "subject": "Wayne Gretzky",   "target_new": {"str": "tennis"}},
}
```

**new:**
```python
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
```

---

### Substitution 8 — Cell 8 fact_probes dict (lines 1853–1872)

**old:**
```python
# Per-fact probe enumeration (consistency + generalization + unmount + 3 shared-spec)
fact_probes = {
    "cfb-001": {
        "consistency":  ["p-cfb-001-cons-1", "p-cfb-001-cons-2", "p-cfb-001-cons-3"],
        "generalization": ["p-cfb-001-gen-1", "p-cfb-001-gen-2", "p-cfb-001-gen-3"],
        "specificity_per_fact": [],  # polysemy probe DROPPED per D-S25-1
        "unmount": ["p-cfb-001-unmount-1"],
    },
    "cfb-002": {
        "consistency":  ["p-cfb-002-cons-1", "p-cfb-002-cons-2", "p-cfb-002-cons-3"],
        "generalization": ["p-cfb-002-gen-1", "p-cfb-002-gen-2", "p-cfb-002-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-002-unmount-1"],
    },
    "cfb-003": {
        "consistency":  ["p-cfb-003-cons-1", "p-cfb-003-cons-2", "p-cfb-003-cons-3"],
        "generalization": ["p-cfb-003-gen-1", "p-cfb-003-gen-2", "p-cfb-003-gen-3"],
        "specificity_per_fact": [],
        "unmount": ["p-cfb-003-unmount-1"],
    },
}
```

**new:**
```python
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
```

---

## §3 — Post-application verification predicate

After applying all eight substitutions, run this verification on the amended runbook source (does not require pod execution):

```bash
# In runbook source directory
RUNBOOK=/workspace/runbooks/stage_1_sect_runbook_v1_4.md

# Substitution-completion checks
echo "== Verifying S2.12-A amendment application =="

# All v1 fact_ids should be removed from the executable cells (Cells 6, 7, 8)
# (note: v1 fact_ids may persist in narrative documentation tables and §10/§11
#  references — those are NOT in scope for this amendment)
grep -n '"cfb-001"\|"cfb-002"\|"cfb-003"' "$RUNBOOK" \
    | grep -v '^[[:space:]]*#\|^|\|stage_1_trial_cfb-' \
    | head -20

# v2 fact_ids should be present in the substituted cells
grep -c '"cfb-v2-001"' "$RUNBOOK"   # expected: >= 8 (Cell 6 dict, Cell 7 active_probes 7 entries, Cell 7 lookup, Cell 8 dicts)
grep -c '"cfb-v2-005"' "$RUNBOOK"   # expected: >= 8

# v2 probe count
grep -c '"p-cfb-v2-' "$RUNBOOK"     # expected: 35 (5 facts × 7 probes)

# Variant template handling for cfb-v2-003
grep -c 'competes in the sport of' "$RUNBOOK"  # expected: >= 2 (Cell 7 lookup, Cell 8 fact_memit_requests)
grep -c 'competes in the game of' "$RUNBOOK"   # expected: >= 1 (Cell 7 cons-1)

# Amendment markers
grep -c 'S2.12-A AMENDMENT' "$RUNBOOK"  # expected: 6 (one marker per substitution that adds a comment)
```

Expected verification output:
- v1 fact_id residue in executable cells: 0 (some narrative-doc lines may still reference "cfb-001/002/003" — out of scope, OK to leave)
- `cfb-v2-001` count: ≥ 8
- `cfb-v2-005` count: ≥ 8
- `p-cfb-v2-` total: 35
- `competes in the sport of`: ≥ 2
- `competes in the game of`: ≥ 1
- `S2.12-A AMENDMENT` markers: 6

If any check fails, identify which substitution did not apply correctly and reapply.

---

## §4 — Out-of-scope (narrative documentation drift)

The runbook contains narrative documentation tables that reference v1 fact_ids in §10 / §11 / §13 / §15 (post-trial-loop discussion sections). These references are out of scope for this amendment because:

1. They are documentation, not executable cells
2. They reference v1's empirical history (S2.8 forensic findings, S2.5 capture verdicts) which is correct as historical record
3. Updating them would conflate executable-state amendments with documentation-state revisions

Examples of out-of-scope drift:
- Lines 2860–2874: Probe-set summary table referencing v1 fact_ids (historical reference)
- Lines 2922–2940: NV state directory layout showing `cfb-001/r1/`, etc. (will be regenerated at execution time as `cfb-v2-001/r1/` etc.; layout document is for reference)
- Line 2779: "Per-fact retrospective: was cfb-003 BPE-fragmentation impact (OQ-S25-7) detectable in trial verdicts?" — historical question still valid as anchor for OQ-S25-7 carry-forward

These references will be reconciled at runbook re-versioning (v1.4 → v1.5 hardening pass), not at this amendment.

---

## §5 — Application steps

1. Open `/workspace/runbooks/stage_1_sect_runbook_v1_4.md` in an editor
2. Apply substitutions 1–8 in order (§2)
3. Save
4. Run verification (§3); reapply any substitution whose target check fails
5. Sync amended runbook back to KB if desired (operator preference; not required for execution)
6. Cell 0 → Cell 12 execution proceeds with the amended literals

The amendment is reversible — git checkout of the unamended runbook restores the v1 fact set if needed (e.g., for retrospective re-execution against CFB v1).

---

*End of S2.12-A Runbook Amendment Patch.*
