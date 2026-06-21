# B1 — Model-Size Term Pre-Registration (capacity-law size extension)

_Created 2026-06-21. Pre-registration for the **model-size term** of the D1 relation-concentration capacity law (`EXPERIMENT_RUNBOOK.md` §8 B1 / §0.3; extends `docs/D1_CAPACITY_LAW_PREREG.md`). **Criteria FROZEN before any GPU run** (§2.3). DRAFT until: (1) `advisor()` pass [DONE 2026-06-21], (2) operator review (model-axis + disk decision), (3) disk-headroom gate (4B only). Then frozen — no post-hoc threshold edits (§3.1)._

_Supersedes the 4B-only draft `B1_QWEN3_4B_SIZE_TERM_PREREG.md` after advisor surfaced that **Qwen2.5-7B (cached, free) is the cleaner same-generation size axis** and that **ΔW-norm comparability gates the size verdict**._

---

## 0. F1 link — what this closes

D1 (`CORPUS/22`, D-D1-1) established **on Qwen2.5-3B only**: at FIXED total edit count, held-out same-relation (capital) read corruption is driven by **per-relation edit concentration** (capital-edit-count), not global `edge_count_since_anchor` — a small non-negative cross-relation term on top (two-variable law). The §8.7 drift contract therefore must count per-relation concentration. **But every number is N≤50, single model.** F1 needs to know whether the §8.7 envelope (warn/hard thresholds) is **model-size-invariant** or must **scale with model size** — otherwise the spec cannot state a portable safe-write envelope (`D1_CAPACITY_LAW_PREREG.md` §7c "model-size term open — B1").

**B1's deliverable for F1:** a **second model point on the same sequential concentration instrument**, answering: does the concentration→corruption slope change with model size, and in which direction? → fixes whether the §8.7 amendment's thresholds are absolute or size-conditioned.

---

## 1. The decisive falsifiable claim

> **The D1 relation-concentration law (held-out same-relation corruption is a function of per-relation edit-count at fixed total-N) holds on a second, larger model, AND the concentration→corruption slope's dependence on model size is characterized (steeper / equal / shallower vs Qwen2.5-3B), with the comparison validated against per-edit ΔW-norm so the verdict is "size", not "edit-strength".**

---

## 2. Design — model axis + harness

**Two candidate size points (advisor-surfaced; operator selects in the review gate):**

| Point | Size axis | Cost / disk | Adds | Status |
|---|---|---|---|---|
| **Qwen2.5-7B** | 3B→7B, **same generation** = CLEAN size axis | **$0 — model + cov [4-8] both cached, no download, no disk gate** | the cleanest size-term comparison | **PRIMARY — run regardless** |
| **Qwen3-4B** | 3B→4B, size **AND generation** (Qwen2.5→Qwen3) | ~8GB download + ~2.5GB cov; **disk gate (quota dashboard-only)** | cross-generation generality + BetaEdit published-curve anchor + Qwen3 = LARQL-servable deploy family | **OPTIONAL extension — disk-gated** |

For a *size* term, **3B→7B varies size cleanly; 3B→4B varies size and generation** (a confound for the size claim, but a bonus generality/anchor check). Recommendation: **run 7B for the size axis** (free, clean, now); run 4B **if** the operator wants the cross-generation + BetaEdit anchor AND disk clears. The fitted-law caution stands either way (see §5).

**Harness (both points):** port `experiments/track_d/d1_dose_response.py` — the harness that produced the D1 Phase-3 replication — **protocol-identical**; changes are model-binding only (ID/REV/hparams path) **plus the ΔW-norm logging in §2.1**. The `my_edit` / `compute_P` / inertness-gate code is **VERBATIM** (LAW#5, unchanged).

**Recipe (frozen, identical to 3B — NOT re-tuned):** in-solve AlphaEdit, null-space P + cache_c, **thresh 0.005**, **L2=1.0**, band **[4-8]**, `fact_token=subject_last`. Re-tuning would confound the size comparison.
**hparams:** 7B → existing `configs/hparams/qwen25_7b_memit_hparams.json` (verified: layers[4-8], v_loss_layer=27, lm_head untied, down_proj — matches the cached cov). 4B → author `configs/hparams/qwen3_4b_memit_hparams.json` from a `cat` read of the downloaded `config.json` (LAW#4), band [4-8].
**Stimulus:** reuse `configs/screens/g6_screen_qwen3b_v2.json` entity/relation/truth/CF; **re-derive the confident pool at runtime per model** (harness already filters `base_correct` + re-checks `single_tok` against the model's tokenizer). Relations: `capital` (measured), `language` (dilutant).
**Schedule:** sequential, counterfactual-reassignment, identical to D1. **Pools:** disjoint edit vs held-out (baseline-correct capital), per the D1 harness.

**Dose-response (FROZEN, identical to D1 Phase 3):** fixed total-N on a fixed edit-entity pool, same entities every arm; concentrated arm = all-capital staircase (pure held-out-capital-vs-capital-count reference); dose arms split capital/language to hold total-N fixed; within-arm paired cross-relation term (R_pure_k − R_after).

**N / dose adaptivity (the ONE pre-registered size-driven flex):** larger models may know a different number of these countries. **Rule, frozen, per model:**
- Measure `len(base_correct)` at clean base FIRST (cheap, no edits).
- `base_correct ≥ 72` → **TOTAL_N=48, HELDOUT_N=24, DOSES={24,36,42}** (identical to D1 Phase 3 → directly comparable).
- `48 ≤ base_correct < 72` → keep **TOTAL_N=48**, shrink HELDOUT_N to `base_correct−48` (min 12); doses unchanged. Comparison stays at matched **capital-edit-count** (overlay axis), robust to held-out-set-size differences.
- `base_correct < 48` → **HALT**, report (the screen is itself a size×knowledge finding), surface to operator. Do NOT silently drop N below where the 3B comparison is meaningful.

### 2.1 ΔW-norm comparability (advisor gate #1 — ADDED; gates the size verdict's validity)
Fixed `thresh=0.005` keeps the *recipe* fixed but **not edit-strength**: P is `thresh` applied to each model's covariance spectrum; different models (3B inter 11008 / 7B 18944 / 4B ~9728) have different spectra → different null-space fraction → **different per-edit ΔW** → different collateral on the shared relation direction (= held-out corruption). So a raw SIZE-PROTECTS/WORSENS verdict is confounded with per-edit edit-strength. This is the exact C2-band trap ([[pass-label-not-equal-promotable-claim]], `CORPUS/21` named the norm-matched control THE primary gate); the D1 prereg had it (§2) and the 4B-only draft dropped it.
**Required (nearly free, impossible to reconstruct post-hoc):** in the ported harness, log **band-summed per-edit ΔW Frobenius norm** (sum over the 5 layers, per applied edit) for every arm/model. Report held-out corruption against **cumulative ΔW-norm** alongside vs-capital-edit-count. The raw per-model curve is fine for **§8.7 per-model threshold calibration**; any **scientific** "size protects/worsens" claim is promotable **only if it survives ΔW-norm comparability** (corruption-vs-cumulative-ΔW-norm, not just vs edit-count).

**Metrics** (§7.4 5-way split, identical to D1): held-out capital **top-1** (PRIMARY) + held-out granularity; **cumulative ΔW-norm** (§2.1); write-side **retention**; **apply-expression** (capital + language guards ≥95%); within-entity + global locality (supporting).

---

## 3. Pre-registered pass/fail (FROZEN)

**Primary = the model-size term**, read from the **concentrated (pure-capital) staircase** held-out-capital-top-1 vs **capital-edit-count k**, second model vs the D1 Qwen2.5-3B curve at matched k. `slope = (baseline − R_pure at deepest shared k) / k`.

- **REPLICATE-AND-CHARACTERIZE (expected):** concentration corrupts held-out capital (positive control fires) AND the D1 qualitative law holds (more capital-edits → more corruption at fixed total-N, monotone). The **size term** is reported as ONE of, **and labelled CONFOUNDED-by-ΔW-norm unless it survives §2.1**:
  - **SIZE-PROTECTS** — `slope_larger` materially shallower than `slope_3B` (≥1.5× ratio OR ≥20pp less corruption at deepest shared k) AND survives ΔW-norm comparability: bigger model resists concentration corruption → §8.7 thresholds **scale with model size**.
  - **SIZE-INVARIANT** — slopes within 1.5× AND ≤20pp apart at deepest shared k: concentration law size-stable in this range → §8.7 per-relation counter **transfers across sizes** (per-model calibrated, same structure) — cleaner spec story.
  - **SIZE-WORSENS** — mirror of SIZE-PROTECTS: unexpected; de-confound (generation, ΔW-norm) before promoting.
- **CROSS-GENERATION-FALSIFIED (would overturn D1 generality; meaningful mainly on 4B):** concentrated staircase does **NOT** corrupt held-out capital (positive control fails) while edits express (≥95%) and retain → D1 corruption is model-specific. A real negative — must not be hidden; scopes D1.
- **INVALID (not a result):** dilutant/capital expression <95% in any arm; OR `base_correct<48` (HALT per §2); OR LAW#5 gate fails (|Δ|≥0.05 → HALT).

**Cross-relation term (secondary, replicates D1 Phase 3):** within-arm paired R_pure_k − R_after, reported with D1's low-power caveat (sign pattern, not a precise effect size; granularity = 100/HELDOUT_N pp).

**Anti-anchor note:** the 1.5×/20pp bands derive from "what would change the §8.7 spec story" (a smaller difference would not change whether thresholds must be size-scaled), NOT from any observed larger-model number (none seen). Frozen before the run.

---

## 4. Predictions (+direction)
- **REPLICATE most likely** — shared-relation-direction mechanism (§7.1) is architecture-general (Qwen2.5/Llama/Mistral historically).
- **Size direction genuinely uncertain (why we run it):** size-density hypothesis (§8 B1) → larger = slower collapse (SIZE-PROTECTS). BUT old B1 (CORPUS/19) found 7B did NOT fully clean the *batch* path (100→91.7%) → SIZE-INVARIANT is live. Genuine three-way fork.

## 5. Forks / spec ripple
- **SIZE-INVARIANT →** §8.7 amendment: per-relation-concentration counter, **model-agnostic structure**, thresholds calibrated per deployed model. Cleanest F1 story.
- **SIZE-PROTECTS →** §8.7 amendment: per-relation counter **with a model-size-scaled threshold**; F1 states a minimum-viable-model-size envelope (ties [[deployment-target-intel-cpu]]).
- **SIZE-WORSENS / CROSS-GENERATION-FALSIFIED →** de-confound before any amendment; D1 scoped to Qwen2.5 if falsified. No F1 promotion.
- **Deliverable honesty (advisor):** 2 matched points (3B,7B) [+ loose 7B-batch & 4B] = a **DIRECTIONAL size term, NOT a fitted law** (a fitted law needs ≥3 matched points incl. 8B — the queued 3rd). The §8.7 amendment can land **structurally now** (per-relation-concentration counter replaces `edge_count_since_anchor`), with **size-conditionality as the explicitly-open knob** this run sets the direction of. State this plainly to the operator (task says "quantitative law" — deliver the directional term + structural amendment, do not overclaim a 2-point fit).

## 6. LAWs / gates (§2.4)
1. **Engine fingerprint gate** (SHA of `memit/memit_main.py`); 7B & 4B are **wide-intermediate** arms → confirm `grep -c _cov_cpu == 3` (P-VRAM-CPU-SOLVE) before dispatch.
2. **LAW#5 inertness** — `my_edit` "memit" mode reproduces stock `apply_memit_to_model` on a null/identity edit on the new model (|Δ|<0.05) before any science result; gate FAIL → HALT.
3. **Read-source-before-authoring** — 4B hparams from a `cat` of `config.json`; confirm down_proj naming + layer count before band set. (7B hparams pre-verified above.)
4. **One-fix-then-halt** on any harness bug; HALT + diagnostic JSON.
5. **Storage discipline** — 4B disk-headroom gate (§7) before download; never delete outside §3.3 without operator OK.

## 7. Launch gate (before any GPU run)
1. `advisor()` pass — **DONE 2026-06-21** (added §2.1 ΔW-norm; surfaced 7B clean axis; directional-not-fitted framing).
2. Operator review — **model-axis decision (7B / 7B+4B / 4B-only) + (if 4B) disk decision**. [PENDING]
3. **Disk gate (4B only):** quota dashboard-only; §3.3 reclaim spent; only B3 artifacts (~26GB, DONE/reproducible, not pre-authorized) remain. **7B path needs NO disk gate.** [PENDING — operator, 4B only]
4. Freeze criteria (§3).
5. Pre-flight (§3.2): GPU free, /dev/shm 29GB ✓, transformers==4.51.0 pin.
6. Cheap-first per model: (4B: download→hparams-from-config→) measure `base_correct` (no-edit) → branch N per §2 → (4B: cov [4-8]) → LAW#5 gate → dose-response.

## 8. Artifacts (planned)
`experiments/track_b/b1_size_dose_response.py` (port of d1_dose_response.py + ΔW-norm logging, model-parametrized); results `results/b1_qwen25_7b_dose_response_result.json` [+ `b1_qwen3_4b_*` if run]; 4B: `configs/hparams/qwen3_4b_memit_hparams.json`, `covariance_caches/Qwen_Qwen3-4B/`; writeup folds into `CORPUS/22` + §8.7-amendment note; decision `D-B1-2`.
