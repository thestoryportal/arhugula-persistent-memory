# 21 — C2-BAND FALSIFIER (collinearity→corruption editing-relevance, SEQUENTIAL regime)

_Result run 2026-06-19 (autonomy `c2band_falsifier`); **supervised fold-in 2026-06-20**. Builds on G6.1 (`CORPUS/13`) + C2 depth map (`CORPUS/20`). Engine kmeng01/memit UNMODIFIED; in-solve AlphaEdit harness. Artifacts: `experiments/track_c/band_corruption_compare.py` (wrapper) → `experiments/scale/g6_scale_n_param.py` ×2; results `results/c2band_compare_result.json`, `results/g6_scale_n_result_c2band_{base,812}.json`; logs `logs/c2band_c2band_{base,812}.log`. Decision: **D-C2band-1**._

## The question (pre-registered, frozen before launch)
C2 (`CORPUS/20`) measured that same-relation cross-entity key collinearity is U-shaped in depth, **minimum at L8-12** (cos 0.20-0.42) vs the default edit band L4-8 (0.68-0.70). **Falsifier:** if editing in the low-collinearity band **[8-12]** does NOT yield meaningfully higher cross-entity read locality than **[4-8]** on the **SEQUENTIAL** write path (N=100), the collinearity→corruption mechanism is NOT editing-relevant → the C2 lead is falsified for editing. Sequential, not batch: A1 batch already eliminates this corruption (cross-loc ≈98.5%, at ceiling — no headroom); sequential [4-8] sits at ~55-68% with the headroom C2 predicts the band moves.

**Pre-registered label rule** (`logs/pending_findings/01_c2band_falsifier.md`): guard = retention≥95 AND expression≥95 **both arms** (else INVALID); PASS = `corruption_reduction_pp ≥ 5`; PARTIAL = `>1`; FAIL = `≤1`. Thresholds fixed before the run.

## Mechanical result — LABEL = PASS (by the frozen rule)
N=100 (50 entities × {capital, language}), single seed, write order grouped-by-entity, Qwen2.5-3B, sequential.

| metric | [4-8] base | [8-12] band812 | Δ |
|---|---|---|---|
| `unt_cross_loc` (held-out same-rel JS locality; ↑=less corruption) | 67.68 | 86.41 | **+18.73pp** |
| retention (edited-fact top-1) | 98.0 | 96.0 | −2.0 |
| apply-time expression | 100.0 | 100.0 | 0 |
| `unt_within_loc` (edited entity's OTHER attrs, JS) | 95.48 | **77.77** | **−17.71pp** |
| `unt_global_loc` (unrelated facts, JS) | 97.34 | 98.40 | +1.06 |
| held-out same-rel **top-1 correct** (12 entities) | 58.3 (7/12) | 83.3 (10/12) | +25.0pp |

Guard cleared (ret 98/96 ≥95; expr 100/100 ≥95) → not INVALID. `corruption_reduction_pp = 18.73 ≥ 5` → **LABEL = PASS**. On its pre-registered cross-entity JS metric, the falsifier **did not falsify**: editing in the low-collinearity band [8-12] reduces sequential cross-entity read corruption.

## VERDICT — PASS (mechanical), NOT PROMOTED to PROVEN: a **real direction-specific REDISTRIBUTION, underpowered, with an unquantified within-entity cost**
The frozen LABEL is PASS and is recorded as such (pre-registration is not moved post-hoc). But the supervised deep-thinking pass (DISCIPLINE §2) + an independent adversarial review downgrade the *scientific* claim: the PASS cannot be promoted to a canonical PROVEN node. Five load-bearing reasons:

1. **The top-1 corroboration is NOT significant.** Held-out same-relation top-1 = 7/12 → 10/12 (a 3-entity swing); two-sided Fisher exact **p ≈ 0.37**. The metric that *matches the "reads corrupted" claim* (top-1, per §2.3 JS-vs-top-1) does **not** independently confirm the JS result. The PASS rests on the **single-seed JS delta alone**, which has no error bar (n_seeds=1, n_orderings=1) — the ≥5pp threshold was never calibrated against seed/ordering variance.

2. **A within-entity locality confound, monotone across N.** `unt_within_loc` JS collapses 95.48 → 77.77 (−17.71pp); global locality is fine (97.34 → 98.40), so the damage is specifically **within-entity** (the edited entity's other attributes), not unrelated facts. Band [8-12] is **not a free win** — it trades cross-entity isolation for within-entity collateral.

3. **A direction-specific REDISTRIBUTION (descriptive) that rules out a *uniformly* weaker edit — but NOT all under-editing (calibrated by two reviewers).** The within-loc DROP excludes the simplest null: a uniformly weaker edit perturbs *everything* less → both `cross_loc` and `within_loc` would RISE; observed `cross_loc`↑ (67.68→86.41) but `within_loc`↓ (95.48→77.77), so over the JS metrics the perturbation is **redistributed**, not uniformly attenuated. Apply-time expression 100% both arms excludes a *no-op*. **HOWEVER — cross-family reviewer (gpt-5.5, `FIX-FIRST`) correctly narrows this:** the sign pattern does NOT exclude *non-uniform* under-editing, a changed edit **Δ-norm**, or **depth-specific locality-metric artifacts** (a deeper edit has fewer downstream layers to absorb it, which can move JS by itself). "Expression=100%" shows apply-time firing, NOT equal edit *strength/durability* across bands. **Calibrated claim:** redistribution-consistent and *not a uniformly-weaker edit*; the causal question — real band-specific effect vs edit-strength/Δ-norm/depth artifact — is **OPEN until the norm-matched/sham control (de-confounder c) is run.** Observed cost = within-entity perturbation + lower durability (ret 96<98).

4. **The deciding probe was never measured.** The within-entity TOP-1 for *edited* entities was not logged. The available proxy — held-out "continent" `top1_stable_vs_pre` = 100% both arms — is measuring stability of predictions that were only **33.3% correct pre-edit in both arms**, i.e. stability of already-wrong reads on a different probe set. It does not adjudicate within-entity damage.

5. **No depth-matched control; bands not magnitude-matched.** No sham/null-edit at each band → the three locality deltas are confounded with **injection depth per se** (a deeper edit has fewer downstream layers to absorb it before the unembedding). No per-band edit-Δ-norm report → the *kind* of redistribution is uncharacterized (NB: it is not a uniformly smaller edit — point 3 refutes that from the within-loc sign). Plus: single seed, single ordering (grouped-by-entity is itself a within-vs-cross confound), N=100 endpoint arbitrary (the cross-loc gap is still growing: 8.65pp@N26 → 12pp@N50 → 18.73pp@N100).

## Deep-thinking yield — the mechanism hypothesis (I-INFER, UNMEASURED)
The cross↑ / within↓ asymmetry suggests depth **rotates the key basis**: relation-clustered at L4-8 (same-relation keys collinear → editing one capital rides the shared relation direction onto held-out capitals → cross-entity bleed; within-entity separable) → **entity-clustered at L8-12** (same-relation keys separate → cross-entity clean, but an edit lands on the entity's shared direction → within-entity collateral). This is the dual of the G6.1 cross-entity problem.

**Falsifiable prediction:** same-entity / different-relation key collinearity (e.g. France:{capital, language, continent}) is **inversely-U in depth — HIGHER at L8-12** than at L4-8. `CORPUS/20` measured only *same-relation* (cross-entity) collinearity; this is unmeasured. Until measured, the *specific* basis-rotation geometry is unconfirmed — the redistribution itself is established (point 3: within-loc FALL excludes a weaker edit; expression 100% excludes under-expression), but whether its geometry is the relation→entity rotation vs some other depth-dependent reorganization is open. → hypothesis register (additive: builds-on C2 mechanism; would-advance D1).

## Disposition (D-C2band-1)
- **C2-band shows a real direction-specific redistribution over the JS locality metrics, but it is underpowered AND not yet shown to be a band-specific causal effect.** Not promoted to a PROVEN node: single seed/ordering (no variance); top-1 leg n.s. (p≈0.37); within-entity top-1 cost unmeasured; and — per the cross-family review — edit-strength/Δ-norm/depth-metric confounds are NOT yet excluded (only a *uniformly* weaker edit is). The cross↑/within↓ pattern is established descriptively; whether it is the C2 band lever (vs an edit-strength/depth artifact) awaits de-confounder (c).
- **Not a deployment recipe change.** Deployment uses the BATCH/Genesis path (A1), already clean at [4-8] with within-loc intact. Band [8-12] only bears on the SEQUENTIAL/incremental path (PARKED, D-SCOPE-1). The value here is **mechanistic** — it feeds D1 (capacity law) and the C15 layer-band spec tension (`CORPUS/09`, OQ-W2), **if** de-confounded.
- **Cheapest de-confounders (queued; pre-register + `advisor()` before running). (a)+(b) gate the rest:**
  - (a) **[no GPU edit]** same-entity cross-relation collinearity-vs-depth curve (`compute_ks` activations only, identical pipeline to `CORPUS/20`) → **the MECHANISM gate** (tests D7 basis-rotation, feeds D1); does NOT settle the value/cost question — that's (b).
  - (b) edited-entity within-attribute **TOP-1** logged directly in both arms (re-run) → **the VALUE/cost gate**: does the within-entity JS perturbation flip actual reads, or is the cost distributional-only? Decides "is band[8-12] usable."
  - (c) **★ THE cheapest OVERTURNING control (cross-family reviewer's #1 next step):** per-band edit-Δ-norm report + depth-matched **sham/norm-matched** control. If matching Δ-norm/strength across bands KILLS the cross↑/within↓ pattern, the redistribution claim collapses to an edit-strength/depth artifact → C2-band falsified for editing. This now gates the causal claim ahead of (a)/(b) (which characterize mechanism + cost given a real effect).
  - (d) ≥3 seeds + ≥2 write orderings on the JS delta → gives the ≥5pp threshold a null distribution.

## Cross-family independent review (closes the DISCIPLINE §2.5 independence obligation)
Two independent reviewers, opposite catches — the disposition is the calibrated middle.
- **Opus advisor (same-family, sees transcript):** caught the *first* draft's overclaim "indistinguishable from under-editing" — the within-loc FALL refutes a uniformly-weaker edit (a smaller edit raises both localities). → forced the "redistribution, not a uniformly-weaker edit" correction.
- **gpt-5.5 (cross-family, Codex+ChatGPT-OAuth, evidence-fed, NOT transcript) — verdict `FIX-FIRST`:** concurred "mechanical PASS but NOT PROMOTED" and that the within-cost is undermeasured; but narrowed the claim further — "NOT an under-editing artifact" overshoots, because non-uniform under-editing / Δ-norm / depth-metric confounds remain open. Named the **norm-matched/sham control** as the single cheapest overturning test. Caveat: it could not read local files in-session (read-only sandbox), so it treated the numbers as prompt-provided claims tied to `results/c2band_compare_result.json` — not independently re-derived. (Session: `019ee6ac-…`; `tokens 12,277`.)
- **Net:** both concur on PASS-not-promoted; the causal "real band effect" claim is softened to OPEN-pending-(c). Independence obligation = SATISFIED (a genuinely different model+process, fed the evidence).

## Caveats (kept flush)
12 held-out same-relation entities (top-1 leg underpowered); single seed; single write ordering (grouped-by-entity); Qwen2.5-3B only; N=100; one band pair [4-8] vs [8-12]; locality is JS-distributional (the top-1 leg is n.s.); covariance for L9-12 was computed this run (standing-auth) — not previously cached.

## Process note (a real reversal, logged)
The autonomy driver staged **LABEL = ERROR** ("insufficient wall-clock to start/finish an attempt", `logs/pending_findings/01_c2band_falsifier.md`, 09:37) but the run **completed at 10:01** and produced the result JSONs — a **completed run mislabeled ERROR** because the driver's wall-clock budget expired before its post-run staging fired. Corrected here. Mirrors the E1 "premature conclusive" reversal (`CORPUS/18`): the mechanical autonomy label is a starting point, not a promotable conclusion — supervised review (deep-thinking + independent adversarial pass) is where over-claims are caught. Independence note: the adversarial review was same-model (weak independence, runbook §2.5); a true cross-model advisor-review remains an operator obligation before any upgrade.

## Additive framing (PROGRESS §0.4)
- **builds-on:** G6.1 cross-entity falsifier (`CORPUS/13`); C2 collinearity depth map (`CORPUS/20`).
- **advances:** scale-mechanism chain C → feeds **D1**. **Status delta:** C2-band `OPEN(lead)` → `OPEN(CONFOUNDED, sharpened)`. NOT a deployment recipe change.
- **evidence:** `CORPUS/21`, `D-C2band-1`.
- **additivity check:** moves the C2-band node from "untested lead" to "tested-but-confounded, with the exact de-confounders named," and yields a falsifiable mechanism hypothesis for D1. Does not move the F1 distance by itself (deployment path unaffected); it sharpens a mechanism input.

## FORK
REAL-BUT-UNDERPOWERED → two independent gates. **Value:** (b) edited-entity within-attr top-1 decides whether the redistribution cost flips real within-entity reads (usable vs not). **Mechanism:** (a) collinearity curve decides whether the redistribution is the relation→entity basis rotation (feeds D1 + the C15 reconciliation). If (a) is flat/lower at L8-12, the *basis-rotation explanation* is wrong (some other redistribution geometry) — but the redistribution itself still occurred; it is NOT thereby an under-editing artifact (point 3). Robustness gate either way: ≥3 seeds / ≥2 orderings before any number is promoted.
