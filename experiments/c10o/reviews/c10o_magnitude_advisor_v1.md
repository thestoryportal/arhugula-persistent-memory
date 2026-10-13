FIX-FIRST

Single most important next thing: add a projection-preserving synthetic target/control before implementation, or narrow the label so E2 is “unit direction at original norm,” not fully “direction alone.”

Issues in priority order:

1. **E2 is defensible, but the label overstates what it isolates.** E2 cleanly tests the polar construct “`z_post` unit direction at `z_pre` norm” (`docs/C10O_MAGNITUDE_DIRECTION_PREREG.md:17-18`). But with the rotated group at cosine ≈0.82 and norm ≈1.3x (`CORPUS/47_C10N_ZTRANSPORT.md:21`), E2 necessarily lowers the original `z_pre`-axis projection to about 82% while adding an orthogonal component. Add an E3/EP arm: scale `z_post` so its projection onto `z_pre` equals `||z_pre||` (`z_post * ||z_pre|| / dot(z_post, z_pre/||z_pre||)`). If E2 is low but EP is high, “DIRECTION” is not the right label; the read is projection-retention plus rotation.

2. **Thresholds are mostly defensible as routing labels, not evidence labels.** `f >= 0.6` vs `< 0.3` creates a real dead zone, and `C - B >= 20` prevents partitioning noise from dominating (`docs/C10O_MAGNITUDE_DIRECTION_PREREG.md:30-37`). The caveat: at the minimum contrast, the gray-band is only 6 hits, so keep these as next-arm routing labels only. Do not phrase them as mechanism proof.

3. **The 0.30 displacement split is sound, with one guard.** It is pre-registered from the prior parent result, and the observed parent split is huge: four rows near 0.02 and twenty near 0.73-0.75 (`CORPUS/47_C10N_ZTRANSPORT.md:21`; `results/c10n_ztransport/run.json:2860-2891`, `results/c10n_ztransport/run.json:3046-3051`). Add: if the new run has any rows in a buffer zone, say 0.25-0.35, report a sensitivity read rather than treating the split as clean.

4. **The two-pass consequence is plausible, but too automatic.** A DIRECTION/EITHER label can justify preregistering a two-pass solve as the next cheap arm, but only after the projection-preserving control above does not overturn the read. Also pre-specify the two-pass locality safety now: whether pass 2 is stacked on pass 1 or applied as a fresh edit aimed at `z_post`, the exact A1/A2/L1/L3 gates, and a sham/same-target second-pass control. Injection and weight edit remain different interventions (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:31`), so injection success cannot by itself license locality safety.

5. **§4 needs two more non-claims.** Add: “A DIRECTION/EITHER label does not show a two-pass weight edit will work or remain local,” and “E2 does not distinguish benefit from new orthogonal component from tolerance of reduced original projection unless the projection-preserving arm is included.” The existing non-claims are otherwise good (`docs/C10O_MAGNITUDE_DIRECTION_PREREG.md:42-44`).

Drift check: this advances the live C10 mechanism fork, not F1 closure. The prereg correctly says it is §C write-path / §F post-write diagnostic only and not contract evidence (`docs/C10O_MAGNITUDE_DIRECTION_PREREG.md:5-7`; `docs/SPEC_E2E_GROUND_TRUTH.md:22-30`, `docs/SPEC_E2E_GROUND_TRUTH.md:64-65`).