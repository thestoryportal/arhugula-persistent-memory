# Framework Finding — MEMIT Ceiling Archival — v1.3

**Status:** ADDITIVE AMENDMENT (v1.0 + v1.1 + v1.2 PERMANENT preserved verbatim)
**Supersedes:** none — additive only
**Carry-forward:** S2.28+ sessions inherit v1.0 + v1.1 + v1.2 + v1.3 conjunction
**Predecessor versions:**
- v1.0 (PERMANENT; ratified S2.18 close 2026-05-05) — rank-1-in-weight class ceiling on Llama-3.1-8B; seven axes
- v1.1 (ADDITIVE; ratified S2.18 close 2026-05-05) — ROME elimination amendment (Axis 7)
- v1.2 (ADDITIVE; ratified post-S2.20 codification 2026-05-05) — GRACE adapter-mechanism environmental-conditional ceiling
**This version:**
- v1.3 (ADDITIVE; ratified S2.28 close 2026-06-15) — **Axis 8 (cross-scale, 8B→3B)** + **AKD-confound elimination** + **Axis 9 (band-invariance, [2–6] vs [4–8])**. Promotes the ceiling from "MEMIT-on-Llama-3.1-8B property under our config choices" to "config-independent MEMIT-on-base-Llama property across scale and across the two contested layer bands."

---

## §0. Amendment Scope

### §0.1 Statement

v1.3 documents the T.1 cross-scale execution arc (S2.22 / S2.24) and the T.1-α/β config-variation arc (S2.25 / S2.26 / S2.27) that ran after v1.2 was sealed. The amendment is **ADDITIVE** — v1.0 + v1.1 + v1.2 integrity preserved verbatim. v1.3 makes three additions to the ceiling characterization:

1. **Axis 8 — cross-scale generalization (S2.24).** MEMIT at canonical hparams on `meta-llama/Llama-3.2-3B` produces `0/5` consistency with the identical internal-vs-external signature. The architectural-invariant ceiling is NOT 8B-specific; it generalizes across Llama-class scale. This is the **first model-variation axis** (Axes 1–7 all varied hparams / corpus / target / probe-locus / layer-set / write-engine on the fixed 8B model).

2. **AKD-confound elimination (S2.26).** The "low-AKD-corpus artifact" hypothesis — the most attractive remaining "it's-just-a-bad-corpus" escape hatch — is **empirically false**. Direct measurement (the first AKD measurement ever taken in the workstream) found cfb-v3, the corpus behind every prior ceiling axis, to be **high-AKD** (band-mean key separation 4.62 at L2–6, ratio 1.05× vs the purpose-built high-AKD cfb-v4). MEMIT had well-separated keys to work with across all prior axes and still produced `0/5`. AKD / key-collision is eliminated as the explanation. This is a **hypothesis-class elimination**, not a numbered ceiling axis (no edit was dispatched — the premise failed at the pre-flight gate).

3. **Axis 9 — band-invariance (S2.27).** The eight-axis ceiling **survives the EasyEdit community-standard `[4,5,6,7,8]` band**, single-variable, on cfb-v3. `0/5` cleared, same four-orders-of-magnitude internal-vs-external miss as the canonical `[2,3,4,5,6]` band; `delta_vs_2_6_floor ≈ 0`. This is the **first config-variation axis** (Axes 1–8 varied everything except the edit-layer band itself, which every prior axis inherited as `[2–6]`). The "wrong layer band" escape hatch is closed.

v1.3 does not retract or modify any v1.0 / v1.1 / v1.2 claim. The v1.2 GRACE environmental-conditional ceiling (§2 of v1.2) stands unchanged; v1.3 records the parallel T.1 cross-scale GRACE result (S2.22) only insofar as it bears on the determinism chain and the eliminability of the v1.2 VRAM ceiling, and does not alter v1.2's mechanism-scope-UNTESTED disposition.

### §0.2 Diff vs Prior Versions

| Surface | v1.0 PERMANENT | v1.1 ADDITIVE | v1.2 ADDITIVE | v1.3 ADDITIVE (this) |
|---|---|---|---|---|
| Class | rank-1-in-weight (MEMIT) | rank-1-in-weight (ROME) | adapter-mechanism (GRACE) | rank-1-in-weight (MEMIT) — config + scale generalization |
| New axes | 1–6 | 7 (ROME) | (none — environmental, off-axis) | 8 (scale 8B→3B) + 9 (band [2–6]→[4–8]) |
| Axis count | 6 | 7 | 7 (unchanged) | **9** |
| Ceiling type | architectural-invariant | architectural-invariant | environmental-conditional | architectural-invariant — extended to config-independent |
| Model coverage | Llama-3.1-8B | Llama-3.1-8B | Llama-3.1-8B | Llama-3.1-8B **+ Llama-3.2-3B** |
| Band coverage | `[2–6]` (implicit) | `[2–6]` | n/a | `[2–6]` **+ `[4–8]`** |
| Confounds eliminated | A/B/C/D, write-engine swap | + ROME | (n/a) | + **AKD / key-collision** + **layer-band placement** |
| Verdict status | EMPIRICALLY VALIDATED | EMPIRICALLY VALIDATED | EMPIRICALLY VALIDATED (environmental scope) | EMPIRICALLY VALIDATED |

### §0.3 Why Additive

The S2.24 / S2.26 / S2.27 results are structurally homogeneous with the v1.0 / v1.1 elimination class (edit dispatched OR confound directly measured; mechanism observed; internal-vs-external signature reproduced) and extend that same architectural-invariant ceiling along new axes. They do not contradict any prior claim, so the discipline is additive accumulation rather than revision:

| Dimension | v1.0 / v1.1 axes | v1.3 axes (8, 9) + AKD elimination |
|---|---|---|
| Mechanism reachability | Edit dispatched; mechanism observed | Axis 8: edit dispatched (0/5). Axis 9: edit dispatched (0/5). AKD: confound measured directly (no edit needed — premise falsified) |
| Signature characterization | Internal objective drives hard; external probe registers nothing | Reproduced exactly on both new axes (~40,000–63,000× internal gain; 3–6 orders-of-magnitude external miss; top-1 never the target) |
| Verdict claim | architectural-invariant ceiling | Same ceiling, extended: config-independent across scale + band |
| Routing implication | Mechanism class / engine eliminated | Confound classes (AKD, band) eliminated; within-regime arms deprioritized; cross-architecture axis (T.3) surfaced as next hypothesis-class |

v1.3 codifies the accumulation without retracting v1.0 / v1.1 / v1.2.

---

## §1. v1.0 + v1.1 + v1.2 Carry-Forward (Statements Preserved Verbatim)

### §1.1 v1.0 Architectural-Invariant Ceiling (PERMANENT)

The architectural-invariant ceiling on `Llama-3.1-8B × MEMIT × canonical hyperparameters` is empirically validated across seven independent axes per S2.18 close anchor (LOAD-BEARING; permanent post-S2.18):

| Axis | Source Session |
|---|---|
| 1. Hyperparameter sweep (mom2_update_weight, v_lr) bounded at 0.022 | S2.10 |
| 2. Corpus revision bounded at 1.4–3.8e-5 | S2.12-A |
| 3. Target shift bounded | S2.13-C |
| 4. v_lr fine bounded at 7e-7–5e-5 | S2.14-D D.3 |
| 5. Mediation locus L_M=L2 outside canonical band [4..8] | S2.14-D D.1 |
| 6. Layer-set search L2-L6 bounded at 1.5–2.5e-5 | S2.15-D2 |
| 7. ROME canonical hparams (L17 + L2 compute_v 1.06e-2/1.06e-6) | S2.18 |

The seven-axis ceiling is structural (model × {MEMIT, ROME} × hparams). NOT eliminable by Class A/B/C/D corpus/hparam/target/layer-set hypothesis testing NOR by write-engine swap (MEMIT → ROME).

### §1.2 v1.1 ROME Elimination Amendment (PERMANENT)

T.2 ROME ELIMINATED at canonical hyperparameters per S2.18 close (B-FAIL Cell 13). Both load-bearing axes — L17 (ROME paper precedent) AND L2 (S2.14-D D.1 mediation peak) — produce verdict-FAIL on cfb-v3-001 guitar consistency. (See v1.1 §1.2 for the full L17/L2 verdict table; preserved verbatim there.)

### §1.3 v1.2 Adapter-Mechanism Environmental Ceiling (PERMANENT)

T.2 GRACE on `Llama-3.1-8B × fp16 × RTX 4090 24 GiB × canonical environment` is NOT EXECUTABLE; the ceiling is RESOURCE-class (VRAM exhaustion at backward-pass activation retention), NOT mechanism-class. Mechanism scope remains UNTESTED per D-S220-VERDICT-CONDITIONAL-1. The environmental ceiling is eliminable via smaller model OR alternate hardware OR precision relaxation OR deeper-layer edit. (See v1.2 §2 for the full F-1/F-2/F-3 empirical surface and §2.3 untested-claims table; preserved verbatim there.)

**v1.3 note on v1.2 eliminability:** the v1.2 §2.4 first elimination path (smaller-model retry) was subsequently executed at S2.22 (T.1-GRACE-3B). VRAM peaked at 6.47 GiB vs the projected 9.47 GiB — confirming the v1.2 §2.4 prediction that the OOM ceiling is eliminable by scale. The S2.22 GRACE-3B disposition is hparam-conditional (the discriminator gate at canonical `init_epsilon=1.0`, `key_id=-1` structurally never fires on inference probes) and is recorded in the hypothesis-class ledger (§4.2) and the t_branch decision document, NOT as a new ceiling axis here — it is an adapter-mechanism finding parallel to v1.2, not a rank-1-in-weight ceiling axis. This v1.3 note neither extends nor retracts v1.2's mechanism-scope-UNTESTED claim for the 8B environment.

---

## §2. v1.3 Axis 8 — Cross-Scale Generalization (S2.24)

### §2.1 Statement

MEMIT on `meta-llama/Llama-3.2-3B × fp16 × RTX 4090 × canonical hparams × cfb-v3 × layers [2–6]` produces `CELL8_CONSISTENCY 0/5`. The architectural-invariant ceiling — confirmed across seven axes on Llama-3.1-8B — **generalizes across Llama-class scale (8B → 3B)**. It is NOT 8B-specific. This is the **8th axis** and the **first model-variation axis**.

### §2.2 Empirical Surface

Per-fact consistency surface (canonical prompt, post-edit), Llama-3.2-3B:

| fact | target | pre P(tgt) | post P(tgt) | top-1 now | consistency |
|---|---|---|---|---|---|
| cfb-v3-001 | guitar | 0.000224 | 0.000781 | 279 (" the") | FAIL |
| cfb-v3-002 | piano | 0.000018 | 0.000005 | 813 (" his") | FAIL |
| cfb-v3-003 | violin | 0.000081 | 0.000089 | 279 | FAIL |
| cfb-v3-004 | harp | 0.000221 | 0.000553 | 279 | FAIL |
| cfb-v3-005 | flute | 0.000018 | 0.000662 | 279 | FAIL |

**Signature reproduced exactly:** `compute_z` internal objective improved ~40,000× per fact (guitar avg-prob `1.4e-08 → 5.5e-04` over 25 steps) while external P(target) at the canonical prompt barely moved (guitar `2.2e-04 → 7.8e-04`); top-1 never became the target. z_error ~4.5–5.1/layer; upd_norm 0.40–1.34 vs orig_norm ~86–90. Huge internal progress, four-orders-of-magnitude external miss — the ceiling's defining signature, on a second model.

### §2.3 Trustworthiness Anchor

Checkpoint #2 bit-exact gate PASSED at S2.24 Cell 5 — drift `0.00e+00` across 38 probes, 0 top-1 mismatches. Cross-engine determinism (GRACE→MEMIT) proven on 3B. The `0/5` is the model, not noise.

### §2.4 Scale-Variant Config Idiom (recorded for future Llama-class ports)

The proven 3B MEMIT config is **not bespoke** — it is `json.load(hparams/MEMIT/Llama-3.1-8B.json)` with exactly two structural (non-hparam-tuning) overrides:

1. `v_loss_layer`: 31 → **27** (3B has 28 layers; last-layer index for the tied loss objective). Architecture-dependent (= n_layers − 1).
2. `lm_head_module`: `"lm_head"` → **`"model.embed_tokens"`** (3B `tie_word_embeddings=True`; `lm_head.weight` is not a named parameter — it is tied to `embed_tokens.weight`; `compute_z` only reads this weight, so the tied source is mathematically identical, read-only).

All other 18 fields are inherited verbatim from the 8B canonical JSON (including `layers=[2,3,4,5,6]` as a base-JSON property). Covariance caches are recomputed fresh per model (architecture-keyed). This "load 8B JSON, override minimally" pattern is the canonical scale-variant MEMIT config idiom (D-S227-HPARAM-IDIOM-1). For any tied-embedding model, `lm_head_module=model.embed_tokens` is the single highest-priority adaptation: it is the **first** point of dispatch failure if omitted (`compute_z` raises `LookupError` at the first fact, before `v_loss_layer` is ever exercised) — established when the S2.27 first dispatch aborted on `LookupError: lm_head.weight` and the override resolved it (D-S227-LMHEAD-1).

### §2.5 Scope Boundary (load-bearing for interpretation)

The S2.24 `0/5` was obtained on cfb-v3. At S2.24 close, cfb-v3 was **believed** to be a low-AKD corpus (a known MEMIT stress condition), so the result was caveated as "ceiling generalizes across scale UNDER low-AKD conditions" and could not, at that time, disentangle a model-family ceiling from a low-AKD-corpus ceiling. **§3 (AKD elimination, S2.26) removes this caveat retroactively:** cfb-v3 measured high-AKD, so the S2.24 result stands without the low-AKD qualifier. The Axis-8 claim in its final form is therefore: **the ceiling generalizes 8B→3B on a confirmed well-separated-key corpus.**

---

## §3. v1.3 AKD-Confound Elimination (S2.26)

### §3.1 Statement

The "low-AKD-corpus artifact" hypothesis — that the ceiling is an artifact of degenerate, collapsed MEMIT keys rather than a model property — is **empirically FALSE**. AKD (Average Keys Distance: mean pairwise Euclidean separation of subject-last-token activations at the edit layer, the exact vectors `compute_z` keys on) was measured directly for the first time in the workstream at S2.26 Cell P1 (read-only pre-flight; no edit dispatched). cfb-v3 — the corpus behind every prior ceiling axis (1–8) — is **high-AKD**.

### §3.2 Empirical Surface

Per-layer mean pairwise key distance at the subject-last-token edit site (input to `mlp.down_proj`), Llama-3.2-3B:

| layer | cfb-v3 (control) | cfb-v4 (purpose-built high-AKD) | ratio |
|---|---|---|---|
| 2 | 3.3812 | 3.3711 | 1.00 |
| 3 | 3.9661 | 3.9920 | 1.01 |
| 4 | 4.8381 | 5.4442 | 1.13 |
| 5 | 5.3090 | 5.5046 | 1.04 |
| 6 | 5.6071 | 5.9374 | 1.06 |
| **BAND (L2–6)** | **4.6203** | **4.8499** | **1.05** |

cfb-v3's keys sit 3.4–5.6 apart per layer — essentially the same spread as the corpus deliberately authored to be high-AKD (ratio 1.05×). The 5× separation gate (`C-S225-AKD-1`) FAILED, but not because the high-AKD partner was under-separated (the failure mode the gate was built to catch); rather because **the denominator was never small** — cfb-v3 was high-AKD all along.

Measurement integrity certified at Cell P1-VERIFY: all 10 facts decoded confirm the sampled position is the subject-final token in every case (`P1_VERIFY_OK 10/10`), ruling out an off-by-one that could have spuriously inflated cfb-v3's reading.

### §3.3 Why the Original Intuition Was Wrong (mechanism lesson, reusable)

The workstream had reasoned "5 clustered athletes + 1 identical template → collapsed keys → low AKD." This mis-mapped the MEMIT-Merge literature's failure condition onto the corpus. The MEMIT key is the activation at the **subject's last token**, dominated by **subject identity**. "Jackson / Woods / Sanders / Olajuwon / Vonn" are lexically and representationally distinct tokens; a shared template adds shared *context* but does not collapse a subject-identity-dominated key. The literature's low-AKD trap bites on batches of **near-duplicate subjects**, not on five different famous people sharing a sentence frame. **Subject-domain clustering ≠ key clustering. AKD must be measured (Cell P1 instrument), never assumed from subject-domain similarity** (C-S226-1).

### §3.4 Disposition

AKD / key-collision is **ELIMINATED** as the explanation for the ceiling — by the stronger route than "high-AKD also fails": MEMIT had well-separated keys to work with on cfb-v3 across all eight prior axes and still produced `0/5`. This is a hypothesis-class elimination (no numbered ceiling axis is added, because no edit was dispatched — the premise was falsified at the pre-flight gate). It STRENGTHENS the ceiling by removing the most attractive "bad-corpus" escape hatch. cfb-v4 + its paired probe set are preserved as durable high-AKD alternate-domain assets (D-S226-CFBV4-PRESERVE-1), usable for any non-AKD axis.

---

## §4. v1.3 Axis 9 — Band-Invariance (S2.27)

### §4.1 Statement

MEMIT on `Llama-3.2-3B × cfb-v3 × canonical hparams × layers [4,5,6,7,8]` (the EasyEdit community-standard band for this exact model) produces `CELL8_CONSISTENCY 0/5`, single-variable (band the only changed field). The eight-axis ceiling **survives the community-standard band**. This is the **9th axis** and the **first config-variation axis** — every prior axis (1–8) ran on the inherited `[2–6]` band; none varied the edit-layer band itself.

### §4.2 Why the Band Was the Strongest Remaining Confound

At S2.26, a desk-check (Cell P0) found the workstream's config matches the EasyEdit community-standard Llama-3.2-3B MEMIT config on **13 of 14 fields** — including both independently-derived 3B adaptations (`v_loss_layer=27`, tied `model.embed_tokens`), strong external validation of the 3B port. The **one** disagreement was the layer band: canonical `[2,3,4,5,6]` vs community-standard `[4,5,6,7,8]` — overlap only `{4,5,6}`; the workstream edits `{2,3}` the standard excludes and misses `{7,8}` it includes. With AKD eliminated (§3), the band became the strongest cheap unruled-out structural explanation, and a community-flagged disagreement on the exact model. C-S226-3 recorded it as an open structural confound on **all** prior axes (every one ran on `[2–6]`) that had to be resolved before the ceiling could be called a model property rather than a config artifact.

### §4.3 Empirical Surface

Per-fact post-edit P(target_new) at the canonical prompt, `[4–8]` band, Llama-3.2-3B, cfb-v3:

| fact | target_new | tid | P(target_new) | top-1 now | cleared |
|---|---|---|---|---|---|
| cfb-v3-001 | guitar | 17418 | 7.34e-04 | 279 (` the`) | False |
| cfb-v3-002 | piano | 27374 | 4.47e-06 | 813 (` his`) | False |
| cfb-v3-003 | violin | 63137 | 5.45e-05 | 279 (` the`) | False |
| cfb-v3-004 | harp | 4960 | 1.24e-03 | 813 (` his`) | False |
| cfb-v3-005 | flute | 96812 | 8.54e-04 | 1077 (` her`) | False |

Every `P(target_new)` is 3–6 orders of magnitude below the 0.5 consistency band; top-1 never left the natural answer (` his` / ` her` / ` the`). **`delta_vs_2_6_floor ≈ 0`** — the band swap moved nothing.

### §4.4 Internal-vs-External Signature Reproduction (the load-bearing diagnostic)

The dispatch log shows the **same internal-vs-external split** that defines the ceiling on every prior axis. `compute_z` drove the internal objective hard on every fact, then the external probe registered nothing:

| fact | internal avg-prob (start → end) | internal gain | external P(tgt) | top-1 |
|---|---|---|---|---|
| guitar | 1.1e-08 → 7.1e-04 | ~63,000× | 7.3e-04 | unmoved |
| piano | 1.4e-08 → 7.3e-04 | ~52,000× | 4.5e-06 | unmoved |
| violin | 1.6e-08 → 1.1e-03 | ~69,000× | 5.5e-05 | unmoved |
| harp | 2.9e-06 → 4.7e-03 | ~1,600× | 1.2e-03 | unmoved |
| flute | 1.5e-08 → 5.7e-04 | ~38,000× | 8.5e-04 | unmoved |

The optimizer worked; the model still won't say the new fact when asked. The band reconfigured the mechanism correctly — the log shows `Rewrite layer is 8` (top of `[4–8]`) and `Tying optimization objective to 27`, both correct for the new band — and the outcome did not change. This is the architectural-invariant ceiling signature, reproduced under the community-standard band.

### §4.5 Single-Variable Integrity (how "band-only" was proven)

Every held-constant pillar was mechanically certified, not assumed (S2.27 §3):

- **Model** — Checkpoint #4 bit-exact gate vs the S2.22 GRACE-engine baseline: `drift_max=0.00e+00` (extends the Llama-3.2-3B determinism chain to checkpoint #4).
- **Engine** — SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` verified (REUSE).
- **Patches** — `memit-patches v2.5` P-5/P-6/P-7 all verified live.
- **Reuse caches L4/L5/L6** — SHA-256 byte-identical to S2.26.
- **New caches L7/L8** — byte-equality gate (`C-S227-1`): both exactly `268,436,642` bytes, same `wikipedia`/`100000`/`float32`/`t100` envelope, computed by a 2-line diff of the proven S2.24 script.
- **Hparams** — full 20-field `MEMITHyperParams` diff (`C-S227-2`): only `layers` differs (`[2,3,4,5,6] → [4,5,6,7,8]`).
- **Reversal** — Copy-Unmount restored L4–L8 to `drift_max=0.00e+00` across all 5 facts (5th validated Copy-Unmount layer-range).

The band is the sole variable, proven at the byte and field level.

### §4.6 Disposition

RESOLVES `C-S226-3` (the band confound on all prior axes), AGAINST the band hypothesis. The `[2–6]` vs `[4–8]` disagreement is no longer an open structural confound: the ceiling holds on the community-standard band, single-variable. The eight-axis ceiling was **not** a layer-band artifact. This promotes the ceiling from "model property under our band choice" to "**config-independent across the band axis**" — the first config-variation axis, and the closure of the most attractive remaining "it's-just-a-misconfig" escape hatch.

**Scope boundary:** Axis 9 does NOT make a model-family-universality claim beyond MEMIT-on-base-Llama. T.3 (alternate architecture: Mistral / Qwen) remains the open cross-architecture question (§6). The ceiling at v1.3 is a robust MEMIT-on-base-Llama property across scale (8B→3B) and across the two contested layer bands (`[2–6]` / `[4–8]`).

---

## §5. Updated Ceiling Characterization at v1.3

### §5.1 The Nine-Axis Ceiling

```
Architectural-invariant ceiling at v1.3 — nine axes
═══════════════════════════════════════════════════════════════════════
  Axes 1–6  (v1.0)  MEMIT on Llama-3.1-8B:
       hparam sweep / corpus / target / v_lr / mediation-locus / layer-set
  Axis  7   (v1.1)  ROME on Llama-3.1-8B (L17 + L2)
  ─────────────────────────────────────────────────────────────────────
  Axis  8   (v1.3)  MEMIT on Llama-3.2-3B — FIRST MODEL-VARIATION AXIS
       0/5; signature reproduced; scale 8B→3B
  Axis  9   (v1.3)  MEMIT on Llama-3.2-3B, band [4–8] — FIRST CONFIG-VARIATION AXIS
       0/5; signature reproduced; single-variable; delta_vs_2_6_floor ≈ 0
  ─────────────────────────────────────────────────────────────────────
  Confounds ELIMINATED:
       A / B / C / D (v1.0)           corpus / probe / target / layer-set
       write-engine swap (v1.1)        MEMIT ⇄ ROME (rank-1-in-weight class)
       AKD / key-collision (v1.3)      cfb-v3 measured high-AKD (4.62 band)
       layer-band placement (v1.3)     [2–6] ⇄ [4–8], single-variable 0/5

  Coverage: MEMIT + ROME on base Llama, across {3B, 8B} × {[2–6], [4–8]}
  Property: config-independent across all axes tested; NOT eliminable within
            the MEMIT-on-base-Llama regime by any axis varied to date
═══════════════════════════════════════════════════════════════════════
```

### §5.2 Off-Axis Environmental / Adapter Findings (not part of the nine-axis count)

| Finding | Session | Class | Disposition |
|---|---|---|---|
| GRACE 8B environmental (VRAM) ceiling | S2.20 (v1.2) | environmental-conditional | eliminable; mechanism UNTESTED |
| GRACE-3B environmental eliminability confirmed | S2.22 | environmental | OOM ceiling eliminable by scale (6.47 GiB peak) |
| GRACE-3B discriminator-gate non-firing | S2.22 | adapter-mechanism, hparam-conditional | NON-VIABLE at canonical hparams; not architectural-invariant |

These remain off the rank-1-in-weight nine-axis count. The adapter-mechanism class (GRACE) carries a separate, weaker, hparam-conditional finding and does not contribute a ceiling axis.

### §5.3 What the Ceiling Now Is — and Is Not

| Claim | Status at v1.3 |
|---|---|
| MEMIT cannot consistency-edit base Llama-3.1-8B at canonical hparams (cfb-v3) | EMPIRICALLY VALIDATED (Axes 1–6) |
| Ceiling extends to ROME (rank-1-in-weight class) | EMPIRICALLY VALIDATED (Axis 7) |
| Ceiling generalizes across Llama scale (8B→3B) | EMPIRICALLY VALIDATED (Axis 8) |
| Ceiling is NOT a low-AKD-corpus artifact | EMPIRICALLY VALIDATED (AKD elimination) |
| Ceiling is NOT a layer-band artifact ([2–6] vs [4–8]) | EMPIRICALLY VALIDATED (Axis 9) |
| Ceiling is config-independent across all axes varied to date | EMPIRICALLY VALIDATED (9 axes) |
| Ceiling holds on a non-Llama architecture (Mistral / Qwen) | UNTESTED — T.3 open (§6) |
| Ceiling holds on Instruct (vs base) Llama | UNTESTED — OQ-S225-BASE-INSTRUCT-1 open |
| Ceiling holds on a high-AKD benchmark corpus (KnowEdit) edit | UNTESTED — external-validity arm open |
| Ceiling holds under per-layer-swept optimal band (vs the two contested bands) | UNTESTED — within-regime deeper arm, DEPRIORITIZED (§6) |
| Adapter-mechanism (GRACE) viable at non-canonical hparams | UNTESTED — off-axis (§5.2) |

The ceiling is a **config-independent MEMIT-on-base-Llama property**. It is NOT yet a model-family-universal claim; the only remaining axis that would change its *class* (rather than add a same-class confirmation) is the cross-architecture axis.

---

## §6. Forward — Cross-Architecture Axis vs Within-Regime Deeper Arms

### §6.1 The Routing Question

With nine axes confirmed and both major config confounds (AKD, band) eliminated, the forward question is which axis to run next. Two families remain:

- **Cross-architecture (T.3):** MEMIT on a non-Llama base model (Mistral-7B / Qwen-7B). This is a **new hypothesis-class** axis — it tests whether the ceiling is a Llama-family property or a broader base-model / MEMIT-mechanism property.
- **Within-regime deeper arms:** per-layer sweep (Berkeley recipe) and sequential-vs-joint dispatch. These probe **within** the MEMIT-on-base-Llama regime already 9-axis-confirmed; each would be a 10th/11th axis of the same class (config-variation within the regime) rather than a new hypothesis class.

### §6.2 v1.3 Recommendation (Claude's call, surfaced for the record per standing directive)

**Recommendation: re-scope T.3 (cross-architecture, Mistral-7B as the first arm) INTO WS1 as the next hypothesis-class axis; keep the within-regime deeper arms DEPRIORITIZED.** Detailed in the companion cross-architecture-axis scoping note (deliverable 3). Summary rationale:

1. **Information class.** The 9-axis result has exhausted the *within-Llama* config space's high-value escape hatches. Every remaining within-regime arm (per-layer sweep, sequential-vs-joint) is a same-class confirmation: high prior probability of another `0/5`, low marginal information. T.3 is the only remaining axis that can *change the class* of the finding — it is the difference between "MEMIT can't edit base Llama" and "MEMIT can't edit base decoder LMs at canonical hparams."

2. **The band result re-scopes T.3's cost.** T.3 was flagged out-of-scope WS1 at v1.1 partly because the ceiling was not yet config-robust — a T.3 failure could have been dismissed as a Llama-config artifact carried to a new model. Axis 9 removes that objection: the ceiling is now config-independent on Llama, so a T.3 result is cleanly interpretable. The 9-axis result *lowers the interpretive cost* of T.3 even though the compute cost is unchanged.

3. **Tractability is established.** The 3B arc (S2.22 / S2.24) proved the workstream can stand up a fresh model, derive the structural adaptations (tied embeddings, `v_loss_layer`, fresh caches), and run a clean single-variable dispatch in ~1 session. Mistral-7B / Qwen-7B are comparable lifts; the scale-variant config idiom (§2.4) generalizes (load reference JSON, override architecture-structural fields, recompute caches). VRAM fits the RTX 4090 with headroom at 7B.

### §6.3 Recommended Sequencing

| Priority | Arm | Class | Cost | Rationale |
|---|---|---|---|---|
| 1 | T.3 Mistral-7B MEMIT (cfb-v3, canonical) | cross-architecture (new class) | ~1–2 sessions | Only axis that can change the finding's class; interpretively clean post-Axis-9 |
| 2 | T.3 Qwen-7B MEMIT (cfb-v3, canonical) | cross-architecture (new class) | ~1 session (reuses T.3 scaffold) | Second architecture family; distinguishes Llama-specific from decoder-LM-general |
| 3 (defer) | KnowEdit external-validity arm | external-validity | ~1–2 sessions | Confirms ceiling on a benchmark high-AKD edit corpus; orthogonal to architecture |
| 3 (defer) | base-vs-instruct arm (OQ-S225-BASE-INSTRUCT-1) | confound | ~1 session | Controls the long-open base-vs-instruct confound |
| 4 (deprioritize) | per-layer sweep + sequential-vs-joint | within-regime (same class) | ~1–2 sessions | 10th/11th same-class axes; low marginal information post-Route-A |

### §6.4 What This Recommendation Does NOT Do

It does not commit compute — T.3 entry is a WS1-scoping decision the operator ratifies (or defers) at S2.28 close. It does not foreclose the within-regime arms; they remain available if a T.3 result surprises (e.g., if Mistral CLEARS, the per-layer sweep on Llama becomes immediately relevant again as a "what's different" probe). It does not retract T.3's prior out-of-scope flag unilaterally — it surfaces the case that the flag's premise (config-non-robustness) is now removed, and recommends re-scoping.

---

## §7. Cross-Reference Map

### §7.1 v1.3 Inheritance from Session Decisions

| v1.3 Section | Decision Source |
|---|---|
| §2 Axis 8 statement / surface | D-S224-VERDICT-1; D-S224-ADAPT-1; D-S224-CALIB-1 |
| §2.4 config idiom | D-S227-HPARAM-IDIOM-1; D-S227-LMHEAD-1; C-S224-1; C-S224-2 |
| §2.5 scope boundary | S2.24 §2 caveat (retroactively lifted by §3) |
| §3 AKD elimination | D-S226-VERDICT-1; D-S226-CFBV4-PRESERVE-1; C-S226-1; C-S226-2 |
| §4 Axis 9 statement / surface | D-S227-VERDICT-1; D-S227-V13-1 |
| §4.2 band confound | D-S226-S227-1; C-S226-3; S2.26 P0 (`CELLP0_HPARAM_DIFF_OK 13/14`) |
| §4.5 single-variable integrity | C-S227-1; C-S227-2; C-S227-3 |
| §5.2 off-axis GRACE | S2.22 close (GRACE-3B `ROUTE_A_HALT_MECHANISM_3B`); v1.2 §2 |
| §6 forward routing | S2.27 §9; D-S227-VERDICT-1 (deeper-arm deprioritization) |

### §7.2 Forward References

| v1.3 Section | Consumer |
|---|---|
| §5.1 nine-axis ceiling | t_branch_decision_document v1.2 (§-amendment routing matrix) |
| §6 cross-architecture recommendation | Cross-architecture-axis scoping note (S2.28 deliverable 3); S2.29 entry (if T.3 re-scoped in) |
| §5.3 untested-claims table | any future external-validity / base-instruct / T.3 arm kickoff |

### §7.3 Sibling Cross-References

| v1.3 Anchor | Sibling Document |
|---|---|
| §2 Axis 8 (3B MEMIT) | `t1_alt_model_3b_memit_runbook v0.1`; `session_2_24_summary_block.md` |
| §3 AKD elimination | `cfb-v4-highAKD.yaml v1.0`; `probe-set-v4-highAKD.yaml v1.0`; `t1_alt_model_3b_memit_akd_runbook v0.1`; `session_2_26_summary_block.md` |
| §4 Axis 9 (band) | `t1_band_4_8_runbook v0.1`; `session_2_27_summary_block.md` |
| §5 nine-axis ceiling | t_branch_decision_document v1.2 (routing-matrix consumer) |

---

## §8. Document Status

**Authored:** 2026-06-15 (S2.28 authoring session)
**Ratified:** §2 Axis 8 + §3 AKD elimination + §4 Axis 9 + §5 nine-axis characterization + §6 cross-architecture recommendation
**v1.0 + v1.1 + v1.2 integrity:** PRESERVED VERBATIM (additive amendment discipline; §1 carry-forward statements unmodified)
**Persistence:** `/mnt/user-data/outputs/framework_finding_memit_ceiling_archival-v1_3.md`
**Successor:** v1.4 (conditional on next axis verdict — T.3 cross-architecture if re-scoped in, else external-validity / base-instruct arm)

*End of framework_finding_memit_ceiling_archival v1.3 additive amendment — Axis 8 (cross-scale 8B→3B, S2.24) + AKD-confound elimination (S2.26) + Axis 9 (band-invariance [2–6]→[4–8], S2.27); ceiling promoted to config-independent MEMIT-on-base-Llama property across scale and band; v1.0/v1.1/v1.2 PERMANENT integrity preserved verbatim.*
