> **⛔ SUPERSEDED 2026-06-21 by `docs/B1_SIZE_TERM_PREREG.md`** — advisor surfaced that Qwen2.5-7B (cached, free, same-generation) is the cleaner size axis and that ΔW-norm comparability gates the size verdict. Use the new doc. This 4B-only draft is kept only for history (rm is deny-listed).

# B1 — Qwen3-4B Model-Size Term Pre-Registration (capacity-law size extension)

_Created 2026-06-21. Pre-registration for the **model-size term** of the D1 relation-concentration capacity law (`EXPERIMENT_RUNBOOK.md` §8 B1 / §0.3; extends `docs/D1_CAPACITY_LAW_PREREG.md`). **Criteria below are FROZEN before any GPU run** (§2.3). DRAFT status until: (1) `advisor()` pass, (2) operator review (interactive HIL), (3) disk-headroom gate cleared. Then frozen — no post-hoc threshold edits (§3.1 autonomy rule)._

---

## 0. F1 link — what this closes

D1 (`CORPUS/22`, D-D1-1) established **on Qwen2.5-3B only**: at FIXED total edit count, held-out same-relation (capital) read corruption is driven by **per-relation edit concentration** (capital-edit-count), not global `edge_count_since_anchor` — a small non-negative cross-relation term on top (two-variable law). The §8.7 drift contract therefore must count per-relation concentration. **But every number is N≤50, single model.** The F1 readiness determination needs to know whether the §8.7 envelope (warn/hard thresholds) is **model-size-invariant** or must **scale with model size** — otherwise the spec cannot state a portable safe-write envelope. This is the one open D1 axis (`D1_CAPACITY_LAW_PREREG.md` §7c "model-size term open — B1").

**B1's deliverable for F1:** a **second model point** (Qwen3-4B) on the *same sequential concentration instrument*, answering: does the concentration→corruption slope change with model size, and in which direction? → fixes whether the §8.7 amendment's thresholds are absolute or size-conditioned.

---

## 1. The decisive falsifiable claim

> **The D1 relation-concentration law (held-out same-relation corruption is a function of per-relation edit-count at fixed total-N) holds on a second, larger, different-generation model (Qwen3-4B), AND the concentration→corruption slope's dependence on model size is characterized (steeper / equal / shallower vs Qwen2.5-3B).**

Two anchors already bound the size axis loosely: **Qwen2.5-3B collapses** (D1: held-out capital 100%→~24-51% under concentration); **Qwen2.5-7B is the clean reference** (A0/CORPUS/19 — but on the *batch* path / a different instrument, so a loose anchor only). Qwen3-4B is intermediate in size **and** a different generation (Qwen3 ≠ Qwen2.5), so it doubles as a cross-generation generality check on the central OQ-W1 reconciliation. BetaEdit validates editing on Qwen3-4B at band [4-8] (our exact setup) — the natural scale/comparison model (D-B1-1, runbook §5.1).

---

## 2. Design

**Port `experiments/track_d/d1_dose_response.py` to Qwen3-4B, protocol-identical** (the harness that produced the D1 Phase-3 replication). Changes are model-binding only:

**Model / engine (frozen):** `Qwen/Qwen3-4B` (pin a revision at download; record SHA). Engine `kmeng01/memit` **UNMODIFIED** + P-VRAM-CPU-SOLVE; in-solve AlphaEdit (null-space P + cache_c, **thresh 0.005**, **L2=1.0** — identical recipe to 3B; NOT re-tuned — re-tuning would confound the size comparison). Harness = `d1_dose_response.py` solve path, **VERBATIM** (LAW#5-inertness-gated, unchanged).
**hparams (frozen at author-time, LAW#4):** `configs/hparams/qwen3_4b_memit_hparams.json`, authored from a `cat` read of the downloaded `config.json` — band **layers [4,5,6,7,8]**, `rewrite_module_tmp = model.layers.{}.mlp.down_proj`, `layer_module_tmp`, `mlp_module_tmp`, `fact_token=subject_last`, `mom2_*` matching the 3B config except dims. Band [4-8] chosen to match the 3B instrument AND the BetaEdit-validated Qwen3-4B setup (NOT re-optimized).
**Stimulus:** reuse `configs/screens/g6_screen_qwen3b_v2.json` entity/relation/truth/CF data; **re-derive the confident pool at runtime for Qwen3-4B** (the harness already filters `base_correct` = entities Qwen3-4B answers correctly on capital at clean base; `single_tok` re-checked against the Qwen3 tokenizer). Relations: `capital` (measured), `language` (dilutant) — the two clean high-cardinality relations from D1 Phase 3.
**Write schedule:** sequential (the runtime/incremental path where corruption appears), counterfactual-reassignment, identical to D1.
**Pools:** disjoint **edit** vs **held-out eval** (baseline-correct capital entities), per the D1 harness (advisor Fix#2/3 already baked in).

**Dose-response (FROZEN, identical structure to D1 Phase 3):** fixed total-N on a fixed edit-entity pool, same entities every arm; concentrated arm = all-capital staircase (the pure held-out-capital-vs-capital-count reference); dose arms split capital/language to hold total-N fixed; within-arm paired cross-relation term (R_pure_k − R_after).

**N / dose adaptivity (the ONE pre-registered size-driven flex):** Qwen3-4B may know a different number of these countries than Qwen2.5-3B → the baseline-correct pool size differs. **Rule, frozen:**
- Measure `len(base_correct)` on Qwen3-4B at clean base FIRST (cheap, no edits).
- If `base_correct ≥ 72` → use **TOTAL_N=48, HELDOUT_N=24, DOSES={24,36,42}** (identical to D1 Phase 3 → directly comparable).
- If `48 ≤ base_correct < 72` → keep **TOTAL_N=48**, shrink HELDOUT_N to `base_correct−48` (min 12); doses unchanged. Comparison stays at matched **capital-edit-count** (the overlay axis), which is robust to held-out-set-size differences.
- If `base_correct < 48` → **HALT** and report: Qwen3-4B lacks the confident pool for a matched-N run; record the partial (the screen itself is a finding about size×knowledge) and surface to operator. Do NOT silently drop N below the level where the 3B comparison is meaningful.

**Metrics** (§7.4 5-way split, identical to D1): held-out capital **top-1 correctness** (PRIMARY) + held-out granularity noted; write-side **retention**; **apply-time expression** (capital + language dilutant guards ≥95%); within-entity + global locality (supporting).

---

## 3. Pre-registered pass/fail (FROZEN)

**Primary deliverable = the model-size term**, read from the **concentrated (pure-capital) staircase** held-out-capital-top-1 vs **capital-edit-count k**, Qwen3-4B vs the D1 Qwen2.5-3B curve at matched k. Define **slope_4B / slope_3B** = (baseline − R_pure at the deepest shared k) / k.

- **REPLICATE-AND-CHARACTERIZE (expected):** concentration corrupts held-out capital on Qwen3-4B (positive control fires), AND the D1 qualitative law holds (more capital-edits → more corruption at fixed total-N, monotone). The **size term** is then reported as one of:
  - **SIZE-PROTECTS** — `slope_4B` materially shallower than `slope_3B` (≥ a 1.5× ratio OR ≥20pp less corruption at the deepest shared k): larger/newer model resists concentration corruption → §8.7 thresholds **scale with model size** (bigger = larger safe envelope).
  - **SIZE-INVARIANT** — slopes within a 1.5× ratio AND ≤20pp apart at the deepest shared k: the concentration law is size-stable in the 3B–4B range → §8.7 per-relation counter **transfers across sizes** (thresholds calibrated per model but same structure) — the cleaner spec story.
  - **SIZE-WORSENS** — `slope_4B` materially steeper (mirror of SIZE-PROTECTS): unexpected; flags an architecture/generation effect, not pure size → de-confound before promoting.
- **CROSS-GENERATION-FALSIFIED (would overturn D1's generality):** on Qwen3-4B the concentrated capital staircase does **NOT** corrupt held-out capital (positive control fails) while edits express (≥95%) and retain — i.e. the D1 concentration corruption is **Qwen2.5-specific**, not a general property. This is a real, publishable negative for the OQ-W1 reconciliation's generality and **must not be hidden** — it would scope D1 to Qwen2.5.
- **INVALID (not a result):** dilutant (language) or capital apply-expression <95% in any arm (false dilution / false no-op); OR `base_correct < 48` (insufficient instrument — HALT per §2); OR LAW#5 inertness gate fails (|Δ|≥0.05 → HALT).

**Cross-relation term (secondary, replicates D1 Phase 3):** within-arm paired R_pure_k − R_after, reported with the same low-power caveat as D1 (sign pattern, not a precise effect size; held-out granularity = 100/HELDOUT_N pp).

**Anti-anchor note:** the 1.5×-ratio / 20pp bands are derived from "what would change the §8.7 spec story" (a <1.5× / <20pp difference would not change whether thresholds must be size-scaled), NOT from any observed 4B number (none seen yet). They are frozen before the run.

---

## 4. Predictions (+direction)
- **REPLICATE most likely** — the shared-relation-direction mechanism (§7.1) is architecture-general (confirmed across Qwen2.5/Llama/Mistral families historically); a different Qwen generation should still show it.
- **Size direction — genuinely uncertain (this is why we run it):** the size-density hypothesis (§8 B1) predicts smaller dense models collapse faster → 4B shallower than 3B (SIZE-PROTECTS). BUT D1's old B1 (CORPUS/19) found 7B did NOT fully clean up on the batch path (100→91.7%), and Qwen3 is a different generation — so SIZE-INVARIANT is a live alternative. Pre-registered as a genuine three-way fork.

## 5. Forks / spec ripple
- **SIZE-INVARIANT →** §8.7 amendment: per-relation-concentration counter, **model-agnostic structure**, thresholds calibrated per deployed model. Cleanest F1 story. → write §8.7 amendment + F1 readiness line.
- **SIZE-PROTECTS →** §8.7 amendment: per-relation counter **with a model-size-scaled threshold**; F1 states a minimum-viable-model-size envelope (ties to [[deployment-target-intel-cpu]] CPU-deploy small-model appeal). → §8.7 + F1 with a size condition.
- **SIZE-WORSENS / CROSS-GENERATION-FALSIFIED →** de-confound (re-tune check, generation vs size) before any §8.7 amendment; D1 scoped to Qwen2.5 if falsified. Surface to operator; no F1 promotion.
- In all promotable cases: this is **2 model points on the matched instrument (3B, 4B)** + a loose 7B anchor → a **DIRECTIONAL size term**, NOT a fitted size law (same calibration caution as D1 §3.1; a fitted law needs ≥3 matched points incl. 8B). Pre-registered as such.

## 6. LAWs / gates (§2.4)
1. **Engine fingerprint gate** before any dispatch (SHA of `memit/memit_main.py`; `grep -c _cov_cpu` as required — Qwen3-4B is a wide-intermediate arm → confirm P-VRAM-CPU-SOLVE count == 3 if required).
2. **LAW#5 inertness** — the `my_edit` "memit" mode must reproduce stock `apply_memit_to_model` on the null/identity edit on Qwen3-4B (|Δ|<0.05) before any science result is trusted. The harness runs this gate every launch; gate FAIL → HALT.
3. **Read-source-before-authoring** — author `qwen3_4b_memit_hparams.json` from a `cat` read of the downloaded `config.json` (NOT from memory of Qwen3 dims); confirm `down_proj` naming + layer count before the band is set.
4. **One-fix-then-halt** on any harness bug; HALT + diagnostic JSON.
5. **Storage discipline** — disk-headroom gate (§7) cleared before download; never delete outside the §3.3 authorized list without operator OK.

## 7. Launch gate (before any GPU run)
1. `advisor()` pass on this pre-registration. [PENDING]
2. Operator review (interactive HIL). [PENDING]
3. **Disk-headroom gate** — quota is dashboard-only; §3.3 reclaim candidates already spent; only B3 artifacts (~26GB) remain reclaimable (not pre-authorized). Confirm headroom OR get operator authorization before the ~8GB download + ~2.5GB cov. [PENDING — operator]
4. Freeze criteria (§3) — no post-hoc threshold changes.
5. Pre-flight (§3.2): GPU free, `/dev/shm` headroom (29GB ✓), transformers==4.51.0 pin present.
6. Cheap-first: download → author+verify hparams → measure `base_correct` (no-edit) → branch N per §2 rule → cov [4-8] → LAW#5 gate → dose-response.

## 8. Artifacts (planned)
`configs/hparams/qwen3_4b_memit_hparams.json`; `experiments/track_b/b1_qwen3_4b_dose_response.py` (port of d1_dose_response.py); `results/b1_qwen3_4b_dose_response_result.json`; cov `covariance_caches/Qwen_Qwen3-4B/`; writeup folds into `CORPUS/22` (D1 capacity law) + a §8.7-amendment note; decision `D-B1-2`.
