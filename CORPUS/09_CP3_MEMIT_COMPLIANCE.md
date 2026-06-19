# 09 — CP3: MEMIT-COMPLIANCE OF THE RECIPE (result)
_Analysis over primary artifacts (2026-06-18). No new run — the evidence is the engine identity, our editing code, our hparams, and the spec text. Two claims at two confidences: (A) D12 method-class = CONFIRMED; (B) C15 layer band = OPEN DIVERGENCE._

## The CP3 question (from 03 line 52)
The spec designates **MEMIT** as the write engine (**D12**) and explicitly excludes **ROME, GRACE, and full
fine-tuning**. CP3: confirm that our recipe — **in-solve AlphaEdit (null-space projection) + preserve-sampling
+ batched compile** — counts as "MEMIT" for D12 compliance, vs. an extension to flag.

## Primary sources used (all on disk — no reliance on the AlphaEdit paper, which is not vendored)
1. **Engine identity** — `memit_dry_run/memit/README.md`: "MEMIT: Mass-Editing Memory in a Transformer", the
   **kmeng01/memit reference implementation**. The base engine literally IS MEMIT.
2. **Our editing code** — `s247_qwen3_recipe.py` / `cp1_governed_write.py` `alpha_edit`:
   `P = U_null U_nullᵀ` from `svd(cov)` keeping small-singular-value directions (null space of preserved-
   knowledge covariance); solve `A = Pi·(K Kᵀ + cache_c) + L2·I`, `B = Pi·K·residᵀ`, `upd = solve(A,B)`;
   `down_proj += upd`; `cache_c += K Kᵀ`. → a **closed-form normal-equation weight delta to FFN down_proj,
   projected into the preserved-knowledge null space**. `compute_z` optimizes the *target vector* (25 steps),
   NOT the weights.
3. **Hparams** — `qwen3_06b_memit_hparams.json` / `qwen25_3b_memit_hparams.json`: `rewrite_module = mlp.down_proj`,
   `mom2_adjustment = true`, `mom2_dataset = wikipedia`.
4. **Spec** — §8.2 lines 311–317 (D12 + C15 + D20).

## (A) D12 method-class — **CONFIRMED (high confidence).** D20 is the spine.
The spec does not say "use MEMIT"; it says **MEMIT with two MANDATORY safeguards (D20): orthogonal projection +
covariance balancer.** This is the decisive frame:

- **Stock 2022 kmeng01-MEMIT has the covariance term but NO orthogonal/null-space projection.** So literal-MEMIT
  **fails D20's orthogonal-projection requirement.** Therefore the spec's "MEMIT" **cannot** mean only-literal-
  2022-MEMIT — it necessarily means the **MEMIT-family closed-form locate-edit *with* the safeguards.**
- Our null-space projector `Pi` is exactly D20 safeguard #1: "new fact vectors computed orthogonally to existing
  feature vectors." It is **not a deviation *from* the spec's MEMIT — it is what brings the recipe *into* D20
  compliance.** The covariance term (`mom2_adjustment`, `cache_c`) is D20 safeguard #2 (the covariance balancer).
- **Defeater for the obvious counterargument** ("null-space projection = AlphaEdit, a post-MEMIT named method,
  so it isn't the designated engine"): literal-MEMIT fails the spec's own mandatory D20 safeguard, so the spec's
  designation logically requires an AlphaEdit-class extension. The extension is **spec-MANDATED, not spec-deviating.**
- **Not the excluded methods:** not **ROME** (single-fact single-layer rank-one; ours is multi-layer band, multi-
  fact, closed-form spread); not **GRACE** (discrete codebook/adapter activated at inference, no covariance-based
  weight edit — note LARQL's CP2 `INSERT`→KNN-store is the GRACE-like path, which is **not** our recipe); not
  **full fine-tuning** (no gradient descent on weights — the weights receive a closed-form delta; only the target
  vector is optimized).
- **preserve-sampling + batched compile are standard MEMIT usage, not method-class changes:** preserve-sampling
  feeds cross-entity anchor keys into MEMIT's *own* preserved-knowledge mechanism (better key sampling, same math);
  batched/joint compile is MEMIT's native "Mass-Editing" batch mode, and the spec itself prescribes L1-buffered
  batch compile (§8.3, T1.2c).

**Verdict (A): the recipe IS "MEMIT" per D12, and additionally satisfies BOTH of D20's mandatory safeguards** —
which stock MEMIT does not. The null-space step is required *for* compliance, not a flag *against* it.

## (B) C15 layer band — **OPEN DIVERGENCE (unresolved; does NOT block D12).**
C15: "MEMIT targets middle-to-late FFN layers (**L15–L25 for a 32-layer model**); early syntax layers are off-
limits for semantic injection." Our band is **[4,5,6,7,8]** for **both** Qwen3-0.6B (28 layers) and Qwen2.5-3B
(36 layers).
- **C15 is stated declaratively, NOT marked provisional.** (The spec's provisional markers — OQ-W1 — attach to
  *drift thresholds*, not to C15. We do not lean on provisional-ness.)
- **The divergence is real under any charitable scaling.** L15–25/32L scaled by depth ≈ L13–22 (28L) or L17–28
  (36L). Our **[4–8] is nowhere near any of these — it is early under every reading** (~14–29% depth on 0.6B,
  ~11–22% on 3B vs. C15's ~47–78%).
- **Passed locality is SUPPORTING evidence, not vindication.** [4–8] edits cleanly across Tiers 1–2 (same-entity
  locality clean, controls preserved, perplexity flat) — but those probes may not surface the polysemantic /
  syntax-layer corruption C15 is specifically guarding against.
- **The honest, interesting tension (surfaced, not resolved):** [4–8] empirically *works* yet *contradicts* C15.
  Either C15's L15–25 numbers are **miscalibrated for small models** (a finding that feeds back to the spec /
  **OQ-W2** "MEMIT/target-model architecture compatibility verification"), or our band is a **genuine gap**. CP3
  does not adjudicate this; it logs it as open.

## Net
- **D12 method-class: CONFIRMED.** Our recipe is MEMIT-family closed-form locate-edit on FFN down_proj, satisfying
  both mandatory D20 safeguards (orthogonal/null-space projection + covariance balancer) — which literal 2022-MEMIT
  does not. ROME/GRACE/fine-tuning are excluded and we are none of them. The AlphaEdit null-space technique is
  **spec-mandated by D20**, not a deviation.
- **C15 layer band: OPEN.** Our empirically-optimal small-model band ([4–8]) diverges from C15's 32-layer
  prescription under any charitable reading. Carried forward as a band-calibration item against the chosen
  deployment model (→ OQ-W2 / G5 / G6), with the live question of whether C15 needs small-model recalibration.
