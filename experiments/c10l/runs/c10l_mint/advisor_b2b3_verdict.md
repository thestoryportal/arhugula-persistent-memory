**PROCEED**

Single most important next thing: write the addendum, but tighten the headline language to “B2/P4 compiled-artifact gate PASS; B3 directional reads UNSUPPORTED,” not broad “deployment viable” or any G/N ordering claim.

1. **Q1: yes, use `N_seed1` vs `G_rep` as replicate 2.** The prereg/readout defines replicate 2 exactly that way; `N_p4` is reported as a seed-0 fourth replicate, not the binding second-seed pair. Numbers: `46-39=+7`, then `34-38=-4`; alternative `42-38=+4` still fails the `>=5/72` rule. Cite: `experiments/track_c/c10l_mint_b3_read.py`, `results/c10l_mint/{arm_N.json,arm_G.json,arm_N_seed1.json,arm_G_rep.json,arm_N_p4.json}`.

2. **Q2: yes, the `0.738` Q4 paraphrase retention is correctly scoped if you keep it as a deployment finding only.** It is paired retention of fp16-GGUF-correct minted prompts: `31/42 = 0.738`; canon is `24/24 = 1.000`. There is no native control and no margin measurement, unlike CORPUS/17’s edited `99/99` vs native-country `75/77` with margin caveat. Cite: `results/c10l_mint/p4_verdict.json`, `CORPUS/17_B3_QUANTIZATION_SURVIVAL.md`.

3. **Main wording fix: “deployment-viable” is a little too fat unless scoped.** Evidence shows added-token preservation through `convert_hf_to_gguf` and Q4_K_M tokenization (`24/24` both), fp16 GGUF parity over `148/148` probed prompts, and Q4 locality intact on L1/L3/unrelated. It does not show E1 ingest, product deployment loop, native parity, or Q4 intrinsic safety. Say: “compiled GGUF artefact viability for the minted-token representation; fp16 GGUF is faithful on this probe set; Q4_K_M trades size for paraphrase recall.”

4. **F-M3 should be rephrased.** “G did not beat N” can stand only as “no robust G-vs-N ordering or init-quality benefit is shown.” Since seed-1 N is below G_rep (`34` vs `38`), avoid language implying N remains directionally better. “The two N seeds straddle G” is the right substance.

5. **Cheapest overturning/control still open:** a third N seed. It would separate random-row geometry/seed spread from the stronger “seed sensitivity” interpretation. Not required by the ruling, but it is the live falsifier for the B3 inference.

Drift check: this advances F1 through C10 option-(iv) deployment viability and the residual C10 wall characterization, but it should not change C10’s OPEN/BLOCKING status.