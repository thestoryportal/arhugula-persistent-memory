FIX-FIRST

Single most important next action: write CORPUS/46 from **run 2 only as binding**, and soften F-D1/F-D3 from causal proof language to diagnostic language.

Specific issues:

1. **Run 1 should not be a “replicate” for Q1/Q2 labels.** The prereg says any validity failure makes the run `INVALID, no reading`; the reader invalidates run 1 because the stored fingerprint lacks `d941a9fb`, even though the execution-time gate plausibly passed. Treat run 1 as **non-binding provenance / sanity echo**, not as a labeled replicate. Run 2 is the binding result: fingerprint hash recorded, Q1 `ABSENT-DOMINANT`, Q2 `H1`, Q3 `SEED-SENSITIVE` (`results/c10m_diag/logs_c10m_chain.log:36`, `:78-83`, `:111-112`; `docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md:36`).

2. **F-D1 over-claims causality.** “The edit’s collateral change at non-keyed positions is sufficient to break the readout” should become: **“The binding edit+inject diagnostic lands in the preregistered H1/collateral bucket: z_pre injection after the edit remains close to edit-only and far below the pre-edit injection control.”** The numbers support that: pre-edit injection `51/72`, edit-only `15/72`, edit+inject z_pre `23/72`, canon `7/24`, which triggers H1 via `K_post <= 12` (`results/c10m_diag/logs_c10m_chain.log:79-82`, `:112`; `docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md:45-49`). They do not isolate which non-keyed position or downstream component is causal.

3. **F-D2 is supported.** Gold-first-token forcing only moves paraphrase from `15/72` to `17/72`, with high-TF constrained-failing subjects `3/24`, so `ABSENT-DOMINANT` follows the frozen thresholds. Avoid “for most subjects nothing of the value is present” unless phrased as “under this constrained greedy paraphrase readout”; teacher-forced evidence is explicitly not contract evidence (`results/c10m_diag/logs_c10m_chain.log:79-81`, `:85-111`; `docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md:38-43`, `:57`).

4. **F-D3’s inference is plausible but over-specific as written.** `z_post` success (`24/24`, `55/72`) supports: **“the edited model still admits a high-performing recomputed target under the same injection procedure.”** The sentence “the solve’s target and realised downstream geometry drift apart” should be labeled as a hypothesis, not the inference. Cheapest separating test: store both `zs_pre` and `zs_post`, then run a 2x2 transport/cosine diagnostic: inject `z_pre` and `z_post` on pre-edit and post-edit models at the same prompts, plus report `||z_post-z_pre||`, cosine, and per-subject success deltas. That separates vector-target drift from “edited-model injection is just a different intervention.”

5. **F-D4 is supported.** Q3 has seed counts `46`, `34`, `36` with the seed-0 fourth replicate `42` listed but not ranged; range over distinct seeds is `12`, meeting `SEED-SENSITIVE` (`results/c10m_diag/logs_c10m_chain.log:78`; `docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md:51-53`).

Drift check: yes, this advances the live C10 mechanism fork, not F1 closure. Keep “C10 stays OPEN/BLOCKING” and “no §5/§6/F1 label change.”