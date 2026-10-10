# 48 — Magnitude or direction: DIRECTION by the frozen routing rule (HIGH-CONTROL); scaling the original target does nothing, the re-solved direction recovers 0.64 of the gap at the original norm and 0.93 with the original projection kept

_Result 2026-10-05. Decision-ID D-C10o-magnitude ⟨D-C10o-magnitude@31389765⟩. Pre-registered `docs/C10O_MAGNITUDE_DIRECTION_PREREG.md` (v2 frozen after the Codex gpt-5.5 design pass; implementation pass; verdict pass before this entry — `results/c10o_magnitude_advisor_{v1,impl,verdict}.md`). Records `results/c10o_magnitude/run.json` (one run, 20:40–21:17), `logs_c10o_chain.log` (full readout with the per-subject table). Driver `experiments/track_c/c10o_magnitude_arms.py` (library reuse of the D-C10m/D-C10n functions; P6 injection hook unchanged); reader `c10o_magnitude_read.py`. Engine unmodified (fingerprint d941a9fb stored in full; LAW#5 |Δexpr| 0.0). LAW#3 reference: D-C10l-covgeom ⟨D-C10l-covgeom@af2e38f7⟩ run 1 arm A. Lineage: CORPUS/47 F-Z3 (D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩), CORPUS/46 H1 bucket (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩)._

## Claim class
**Pre-registered diagnostic on the program's C10 harness — Qwen2.5-3B fp16 MPS, band 4–8, N = 24, one HIGH-CONTROL process. Its labels are next-arm routing labels from an injection assay, not mechanism evidence and not contract evidence (§8.9); no label in CORPUS/44–47 changes; no bearing on the F1 label. C10 stays OPEN/BLOCKING.**

## VERDICT — DIRECTION (routing label; projection-preserving variant recovers 0.93)

Gates all GREEN: fingerprint; LAW#5; A1 71/72; A7 edit-only canon 8/24, para 12/72 (envelope [5, 18]); cell A canon 24/24, para 51/72 → **HIGH-CONTROL** (≥ 44); full post-restore cell-A repeat identical; L1 0/12, `described_as` 87.4, L3 30/30. Rotated population 20 subjects (normalized displacement 0.735–0.751), identical-target 4 (0.021–0.027), buffer zone [0.25, 0.35] empty → no sensitivity read needed. Norm ratio on the rotated twenty 1.28–1.37; `z_post`'s component along `z_pre` is 1.05–1.16 × ‖`z_pre`‖.

| target injected (rotated population) | edited model, para /60 | canon /20 | unedited model (after restore), para /60 | canon /20 |
|---|---|---|---|---|
| `z_pre` (B / A) | 6 | 4 | 42 | 20 |
| `z_post` (C) | 50 | 20 | — | — |
| E1 magnitude: `z_pre` at ‖`z_post`‖ | 5 | 4 | 38 (E1′) | 20 |
| E2 direction: `z_post` at ‖`z_pre`‖ | 34 | 19 | 17 (E2′) | 9 |
| E3 projection-preserving: `z_post` · ‖`z_pre`‖ / ⟨`z_post`, ẑ_pre⟩ | 47 | 20 | 23 (E3′) | 12 |

Identical-target subjects (4): 10–11/12 in every cell. All-subject totals /72: B 17, C 60, E1 15, E2 45, E3 58; A 51, E1′ 47, E2′ 27, E3′ 33.

**Recovered fractions (rotated population, contrast C − B = 44 ≥ 20):** f1 = −0.023, f2 = 0.636, f3 = 0.932 → **DIRECTION** (f2 ≥ 0.6 and f1 < 0.3; the ROTATION-WITH-PROJECTION branch needs f2 < 0.3 and does not fire). f2 is threshold-close: a two-hit drop in E2 would lose the label — it is a routing label only.

## Findings (scoped: one HIGH-CONTROL process; N = 24; one model; injection assay)

- **F-O1 (EVIDENCE-SHOWS).** Magnitude alone does nothing in this assay: the original direction scaled to the re-solved norm scores 5/60 on the edited model against 6/60 unscaled, while the re-solved target scores 50/60. The re-solved direction carries the recovery: 34/60 at the original norm (0.64 of the gap), 47/60 when its component along the original target is held at ‖`z_pre`‖ (0.93).
- **F-O2 (EVIDENCE-SHOWS, injection assay).** The edited model decodes the `z_post`-derived directions far better than `z_pre` (C/E2/E3 = 50/34/47 vs B/E1 = 6/5), while the unedited model decodes `z_pre` and its magnitude-scaled form better than the rotated forms (A/E1′ = 42/38 vs E2′/E3′ = 17/23). This is what the assay shows; it does not establish a general mechanism by which each model "wants" a direction.
- **F-O3 (EVIDENCE-SHOWS, method).** Which four subjects keep an identical target varies per process with where the edit lands (here Zorbland, Brinduun, Skornwell, Pradnoll; in CORPUS/47 Thelby instead of Skornwell); the pre-registered displacement split separated the groups cleanly in both processes (0.02 vs 0.74, no buffer rows).

## What this changes

- **Routing:** DIRECTION → the next mechanism arm is the **two-pass solve** pre-specified in the prereg (§3): a fresh second edit from the base weights aimed at `z_post`; the stacked variant as a reported secondary; a sham second fresh edit aimed at `z_pre` to separate "a second edit" from "a new target"; gates A1 ≥ 68/72, A2 ≥ 68/72, L1 ≤ baseline + 1, `described_as` ≥ baseline − 3, L3 ≥ 29/30, generic perplexity within the CORPUS/44 range. Engine untouched; runs before I-1 OverTone / I-2 forward replay. It is the cheapest falsifier of this routing because it tests whether the direction read survives as a weight edit. Injection success does not license its locality; the gates do (CORPUS/44 F-A3). A second C10o replicate is optional, only if robustness on the threshold-close f2 is wanted before spending the two-pass run.
- CORPUS/46's H1 bucket and CORPUS/47's TARGET-PORTABLE reading stand; this entry adds the component the re-solved target carries.
- Not written here, by the advisor's instruction: "each model wants its own direction" as a mechanism; which positions or components rotate the direction; "the solve under-shot"; contract evidence; any CORPUS/44–47 label change; that the two-pass edit will work or remain local; any F1 change.
- Limitations: one process (HIGH-CONTROL); N = 24; one model (D-C10k-rulings-2); fp16 MPS; the rotated population is 20 subjects, so each fraction moves by 0.023 per hit.


⟨D-C10l-covgeom@0caeca4f⟩
