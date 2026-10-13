**FIX-FIRST.**

Single most important next thing: fix the promotion package before leaning on it. The result doc says `CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md` exists, but that file is absent, and `python3 -B tools/closeout_check.py D-C10k-route-a` reports 14 missing tracker entries. Either remove the premature CORPUS/close-out claim or complete the close-out before treating this as promoted evidence.

Issues, in priority order:

1. **Promotion state is false as written.**  
   `docs/C10K_ROUTEA_RESULT.md:108` claims a CORPUS entry; `CORPUS/42...` is not present, and the closeout gate says `NOT done`. This is a blocker for CORPUS promotion, not a blocker for the halt interpretation.

2. **The halt verdict itself holds.**  
   The prereg requires A1/A2 `para_full ≥ 80` before A7 interpretation; raw results show `0/72` paraphrase at both `L2=10` and `L2=0.01` for A1/A2, with canonical recovered only after rescale (`results/c10k_route_a/R1_w1_*.json`). So `HALTED — CONTROLS_NOT_RECOVERED` is the right scientific label.

3. **F3 is correctly narrowed, but keep it that way.**  
   The observed fact is strong: prompt-last-token AnyEdit gives `0/72` paraphrase despite `24/24` canonical after rescale (`R1_w1_A1_single.json`, `R1_w1_A2_coherent2.json`), and the keying code does use `lookup_idxs = [ex_len - len(current_target_ids)]` (`external_prior_art/AnyEdit_mps/AlphaEdit_ARE/compute_z.py:86-91`). The causal claim still needs the planned keying ablation (`docs/C10K_KEYING_ABLATION_PREREG.md`).

4. **F4 is supported only in its scoped form.**  
   fp64 reproduces the locality damage at `L2=0.01` (`generic_nll_delta 0.25844`, `real_js 84.58`, `para 0/72`; `results/c10k_route_a/fp64_resolve_control.json`), so this is not a fp32 artifact. But it remains “magnitude for prompt-last-token writes,” not a general write-magnitude law.

5. **F6 now looks adequately corrected.**  
   The fp64 `memit_ARE` pass still fits only `2/24` canonical with final z error `88.164`, and ridge diagnostics show single-key gains around `0.036–0.047` at upstream `15000·C` (`fp64_resolve_control.json`, `memit_ridge_diag.json`). That supports “over-regularised for these last-token keys,” not the earlier “numeric degeneracy” story.

Drift check: this advances F1 only as a scoped negative on the local AnyEdit Route A port and as a mechanism lead for the keying-locus ablation. It does not close C10 or license any A7 conclusion.
