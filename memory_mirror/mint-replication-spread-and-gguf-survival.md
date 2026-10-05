---
name: mint-replication-spread-and-gguf-survival
description: "C10L mint (CORPUS/45 addendum, 2026-10-05): minted-token arms spread ±4/72 across processes but 12/72 across N seeds, so directional sub-reads need ≥3 seeds; a minted row survives convert_hf_to_gguf + Q4_K_M as a single id (fp16 GGUF parity 148/148; Q4 paraphrase retention 0.738); torch.pca_lowrank is unseeded"
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

Under D-C10l-rulings-1 the mint result was replicated (prereg §10 B3) and compiled (B2/P4). Five mint replicates read 34–46/72 (N seed 0: 46, 42; G: 39, 38; N seed 1: 34); the two pre-registered directional rules (N − G ≥ 5 in both replicates; min(mint) − max(rare) ≥ 10) both read UNSUPPORTED while the PARTIAL label reproduced every time. P4: both GGUFs tokenise the 24 minted ids as single tokens, the fp16 GGUF matches the HF edit's top-1 id on all 148 probed prompts, Q4_K_M keeps canon 24/24 and paraphrase 31/42 with locality intact.

**Why:** a one-seed ordering between two inits on this harness is inside the seed-to-seed spread (12/72), so "N ≥ G" style sub-reads need three or more seeds before they are written; and the deployment question for a minted token (ruling 3's Git/.vindex artefact) is answered at the compile step, with Q4_K_M costing about a quarter of the paraphrase recall.

**How to apply:** pre-register ≥ 3 seeds (or report only the label, never the ordering) for any init comparison on the mint harness; ship the fp16 GGUF unless size forces Q4_K_M; `torch.pca_lowrank` is unseeded, so hash and keep the saved init tensor (`inits/G.pt`) as the artefact, never re-derive it from the recipe. Reader: `experiments/track_c/c10l_mint_b3_read.py`. See [[c10l-mint-token]] / CORPUS/45.
