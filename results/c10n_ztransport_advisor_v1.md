FIX-FIRST

Single most important next action: tighten §3 before implementation: make the separator behavior-primary, add normalized target displacement `||z_post - z_pre|| / ||z_pre||` as the geometry statistic, and require a full post-restore repeat of cell A before cell D.

Issues in priority order:

1. **Cosine-only geometry gate is the wrong real criterion.** `D ≤ A − 20` is behaviorally defensible against the observed A/C spread: A is 51/72 binding and 54/72 provenance, C is 55/72 binding and 60/72 provenance, so a 20-count gap is much larger than the observed process movement. But mean cosine `< 0.90` is not sufficient as the geometry criterion because it ignores norm-scale drift; §1 already says norms and `||z_post − z_pre||` will be reported, but §3 gates DRIFT only on cosine. Use normalized displacement in the rule, or make geometry descriptive and let D carry the label. `docs/C10N_ZTRANSPORT_PREREG.md:18`, `docs/C10N_ZTRANSPORT_PREREG.md:39`; evidence: `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:14-18`, `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:26`, `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:34`.

2. **Repeat the whole A sweep after restore, not four subjects.** Measuring D after `H.main()` is sound in principle: hooks run while the edit is still applied, and `run_recipe` restores layers at the end. But a four-subject row match is a weak observation-layer check for a 24-subject D claim. Full A repeat is cheap relative to the run and directly verifies the same observation surface D depends on. `experiments/track_c/c10e_bandknob.py:478-490`, `experiments/track_c/c10e_bandknob.py:155-160`, `docs/C10N_ZTRANSPORT_PREREG.md:27`, `experiments/track_c/c10m_diag_arms.py:85-97`.

3. **The replication clause needs an absolute C floor.** `B ≤ A − 20` is fine for reproducing the H1 bucket, but `C ≥ A − 10` alone can pass a flattering weak C if A barely clears validity. Add `C ≥ 44/72` or similar, matching the injection-control validity floor, so “z_post carries the value” cannot mean a low-30s result. Current text: `docs/C10N_ZTRANSPORT_PREREG.md:34-40`; prior control floor: `docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md:36`; observed C: `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:18`.

4. **Rename or narrow TARGET-QUALITY.** `D ≥ A − 10` shows z_post is portable to the unedited model; it does not prove `z_pre` “under-shot” or that the solve objective is defective. That is an inference requiring solve-side checks. Safer label: `TARGET-PORTABLE`, with consequence “run solve-side diagnostics first.” `docs/C10N_ZTRANSPORT_PREREG.md:11`, `docs/C10N_ZTRANSPORT_PREREG.md:40`, `docs/C10N_ZTRANSPORT_PREREG.md:43`.

5. **§4 is mostly good, but add one non-claim.** It already blocks contract evidence, F1 movement, “edit destroys target,” and position claims. Add that neither DRIFT nor TARGET-QUALITY proves a mechanism about compute_z quality, projector failure, or generated-token positions; it only licenses the next diagnostic fork. `docs/C10N_ZTRANSPORT_PREREG.md:45-47`.

Drift check: yes, this advances the live C10 mechanism fork, not F1 closure. Keep the “C10 stays OPEN/BLOCKING” framing.