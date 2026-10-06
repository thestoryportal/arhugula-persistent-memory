# Pre-registration — D-C10o-magnitude: after the edit, does the keyed target need more magnitude, a different direction, or both? (v2 FROZEN, 2026-10-05)

**Status: v2 FROZEN after the Codex gpt-5.5 design pass (`results/c10o_magnitude_advisor_v1.md`, FIX-FIRST: five items folded — E3 projection-preserving target, routing-only labels, buffer-zone sensitivity, two-pass arm pre-specified with locality gates and a sham control, two non-claims). Implementation review next; nothing has run.** Decision-ID `D-C10o-magnitude`. Lineage: CORPUS/47 F-Z2/F-Z3 (D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩, H-C10n-magnitude), CORPUS/46 H1 bucket (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩), CORPUS/39 (strength knobs as weight edits: no rescue). Rulings in force: D-C10l-rulings-2 (diagnostics before mechanism changes), D-C10k-rulings-2 (Qwen2.5-3B only).

## 0. Where this sits, and what it is not

A one-run diagnostic on the **§C write path** read through **§F post-write verification**, the last solve-side read before an engine-path arm: it asks which component of the re-solved target restores decoding on the edited model. Not contract evidence (§8.9); no label in CORPUS/44–47 changes; no bearing on the F1 label. C10 stays OPEN/BLOCKING.

## 1. The question and the cells

CORPUS/47: for twenty of 24 subjects the target the edited model wants is ≈ 30 % longer than the solve's target and rotated from it (cosine ≈ 0.82); the original target decodes 3/60 on those subjects after the edit, the re-solved one 51/60. Two factors are confounded in that contrast — magnitude and direction. Two synthetic targets separate them, each injected into the **edited** model at the subject-last token with the P6 hook:

| target injected into the edited model | what it isolates |
|---|---|
| **B** `z_pre` (as solved) | reference (CORPUS/46–47: 13–23/72) |
| **C** `z_post` (re-solved on the edited model) | reference (55–61/72) |
| **E1** `z_pre · r_s`, with `r_s = ‖z_post‖ / ‖z_pre‖` per subject | magnitude alone (original direction, re-solved norm) |
| **E2** `z_post · (‖z_pre‖ / ‖z_post‖)` | unit direction of the re-solved target at the original norm (its projection onto `z_pre` falls to ≈ 82 % of ‖`z_pre`‖ while an orthogonal component is added) |
| **E3** `z_post · ‖z_pre‖ / ⟨z_post, ẑ_pre⟩` | projection-preserving: the re-solved direction scaled so its component along `z_pre` equals ‖`z_pre`‖ (advisor item 1 — separates "the new orthogonal component helps" from "the reduced original projection is tolerated") |

Reported, not labelled: **A** `z_pre` on the unedited model (the control stratum, N1 of CORPUS/47) and, after the harness restores the base weights, **E1′**, **E2′** and **E3′** on the unedited model (whether the synthetic targets are portable too).

**Population.** The cells are read on the **rotated population**: subjects whose in-process normalized displacement ‖`z_post` − `z_pre`‖ / ‖`z_pre`‖ exceeds 0.30 (midway between CORPUS/47's two clusters, 0.02 and 0.74; expected ≈ 20). The identical-target subjects (displacement ≤ 0.30) have `r_s ≈ 1` and the same direction, so E1 ≈ E2 ≈ E3 ≈ B ≈ C on them; they are reported separately and do not enter the labels. **Buffer zone (advisor item 3):** any subject with displacement in [0.25, 0.35] is flagged; the labels are then also computed with those subjects excluded (a sensitivity read), and the entry reports both — the split is not treated as clean if the two reads differ. Counts are /3 per subject, summed over the population (denominator = 3 × population size).

## 2. Design (one process, baseline recipe, arms A1 + A7, engine unmodified)

Driver `experiments/track_c/c10o_magnitude_arms.py` (library reuse of the D-C10m/D-C10n functions; one new function builds the two synthetic targets). Pre-edit: fingerprint (full output), `z_pre`, cell A. Edit: the harness's own `my_edit`, LAW#5 gate. Post-edit hook (edit applied): `z_post`; cells B, C, E1, E2, E3; the per-subject geometry; `z_pre`/`z_post` hashes and norms. After `H.main()` (restored weights): the full cell-A repeat (must match the pre-edit rows on (subj, val, rows)), then E1′, E2′, E3′. Output `results/c10o_magnitude/run.json`; reader `experiments/track_c/c10o_magnitude_read.py`. Runtime ≈ 75 min.

## 3. Pre-registered readings (frozen before implementation)

**Validity (any failure → INVALID, no reading):** fingerprint d941a9fb; LAW#5 INERT; A1 ≥ 68/72; A7 edit-only `para_full` in [5, 18], canon in [5, 10]; cell A canon ≥ 22/24 and para ≥ 38/72 (instrument range; HIGH-CONTROL ≥ 44 / LOW-CONTROL 38–43 reported as the stratum, not a gate); restoration identical; L3 ≥ 29/30; rotated population ≥ 12 subjects; and the contrast **C − B ≥ 20** on the rotated population (below that the cells cannot be partitioned — reported as CONTRAST-TOO-SMALL, no label).

**Recovered fractions on the rotated population:** `f1 = (E1 − B) / (C − B)`, `f2 = (E2 − B) / (C − B)`, `f3 = (E3 − B) / (C − B)` (clipped to [0, 1] for the label; raw values reported). These are **next-arm routing labels, not mechanism evidence** (advisor item 2; at the minimum contrast the grey band is six hits).
- **MAGNITUDE** if `f1 ≥ 0.6` and `max(f2, f3) < 0.3`.
- **DIRECTION** if `f2 ≥ 0.6` and `f1 < 0.3` (the unit direction at the original norm suffices).
- **ROTATION-WITH-PROJECTION** if `f3 ≥ 0.6` and `f2 < 0.3` and `f1 < 0.3` (the new orthogonal component helps only when the original projection is kept).
- **EITHER** if `f1 ≥ 0.6` and `max(f2, f3) ≥ 0.6` (magnitude alone and a direction construct alone are each sufficient).
- **NEITHER-ALONE** if `max(f1, f2, f3) < 0.3` (the components must combine).
- **MIXED** otherwise.
Canon (/population) is reported beside every count; E1′/E2′/E3′ are reported with no label.

**What each buys.** MAGNITUDE → the edit attenuates the keyed signal downstream; because magnitude as a *weight-edit* knob already failed (CORPUS/39 strength150, locality intact but no rescue), the next arm is I-2 forward replay or a narrower write, not another strength knob. DIRECTION or ROTATION-WITH-PROJECTION → the required direction rotates under the edit; the cheapest mechanism arm is harness-side and engine-untouched: a **two-pass solve**, pre-registered on its own with the following fixed now (advisor item 4): pass 2 is a **fresh** edit from the base weights aimed at `z_post` (the stacked variant — pass 2 applied on top of pass 1 — is a reported secondary); gates A1 ≥ 68/72 and A2 ≥ 68/72, L1 ≤ baseline + 1, `described_as` ≥ baseline − 3, L3 ≥ 29/30, generic perplexity within the CORPUS/44 range; a **sham control** — a second fresh edit aimed at `z_pre` again — separates "a second edit" from "a new target". Injection success does not license the arm's locality (CORPUS/44 F-A3: injection and the weight edit are different interventions); the gates do. EITHER → the two-pass solve first (cheaper), magnitude as its tie-break. NEITHER-ALONE → I-1 / I-2 on the engine path, as CORPUS/46 already queued. MIXED → report; I-1 / I-2 proceed.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–47 changes. Injection counts are not contract evidence. No claim about *which* non-keyed positions carry the collateral change, about `compute_z` quality, or about the projector. A label here licenses one next arm; it does not show that arm will transfer under paraphrase. A DIRECTION / ROTATION-WITH-PROJECTION / EITHER label does not show that a two-pass weight edit will work or remain local. E2 alone does not distinguish benefit from the new orthogonal component from tolerance of a reduced original projection; only E3 beside it does (advisor item 5). Nothing here can change the F1 label. C10 stays OPEN/BLOCKING.

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON. Engine, LARQL and git unmodified. Close-out through `tools/closeout_check.py D-C10o-magnitude` once the CORPUS entry exists (stamp the source's own IDs before deriving the token).

## 6. Reviews

v1 → Codex gpt-5.5 design pass (`results/c10o_magnitude_advisor_v1.md`, FIX-FIRST, five items folded) → v2 frozen → implementation review → run → verdict pass → CORPUS/48.
