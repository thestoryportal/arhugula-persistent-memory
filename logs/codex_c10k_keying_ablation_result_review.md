FIX-FIRST

Single most important next thing: run the cheapest K3/K4 de-confounder before writing this as a CORPUS finding: log/verify `compute_z` target success for the last-token cells, then rerun a non-colliding-KL or reduced-ridge no-projector K3 cell if needed. Right now the “ridge prevents writability” mechanism is plausible, but not nailed down.

Specific issues, in priority order:

1. The result does not answer the preregistered keying-generalisation criterion. It correctly declares K3/K4 invalid because canon is below 90 (`K3`: A1 29.2, A2 4.2; `K4`: A1 25.0, A2 8.3 in `results/c10k_keying_ablation/K3.json` and `K4.json`). So the safe reading is: last-token cells failed to write under this construction. No keying-generalisation rule is licensed.

2. “Last-token keys are not writable under the Wikipedia covariance ridge” is still over-claimed. K3/K4 changed the subject string so the MEMIT KL prompt becomes `"<country> is the city of is a"` per `experiments/track_c/c10e_bandknob.py`, while using `kl_factor=0.0625` and `mom2_update_weight=5000` from `configs/hparams/qwen25_3b_memit_hparams.json`. The artifacts I saw do not log K3/K4 z-target success, so a z/KL conflict remains a live confound.

3. The ridge diagnostic supports the mechanism but does not close it behaviorally. `results/c10k_route_a/memit_ridge_diag.json` shows ridge/key ratios of 132, 181, 65, 37, 17 and weak gains around 0.056, 0.048, 0.048, 0.068, 0.069 at weight 5000. Good evidence for the ridge story; not by itself proof that this K3/K4 behavioral failure is caused by ridge rather than the K3/K4 z/KL construction.

4. The Route A “complementary half” should stay explicitly `I-INFER`. `docs/C10K_ROUTEA_RESULT.md` reports AlphaEdit_ARE L2=0.01 reaches 24/24 canon and 0/72 paraphrase, but that path also changes projector, ridge, objective/module lineage, and dtype. It strengthens suspicion; it does not supply the missing valid MEMIT last-token cell.

5. K2 does hold, but only narrowly: subject-keyed writes without templates still pass the ≥80 paraphrase bar (`K2`: A1 91.7, A2 88.9; canon 100/100). So “templates are not required here” is supported. “Key locus is the carrier” is not supported by this run.

6. Close-out is not done. `CORPUS/43_C10K_KEYING_ABLATION.md` is absent, and `python3 tools/closeout_check.py D-C10k-keying-ablation` reports 13 missing tracker entries. The result draft’s close-out claim is therefore false as of this workspace state.

Drift check: this advances F1 only as a scoped diagnostic on why the C10 keying route remains uncertain. It should not become a new settled evidence node until the K3/K4 writability confound is resolved and the close-out gate passes.
