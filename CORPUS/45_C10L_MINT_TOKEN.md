# 45 — Mint one vocabulary token per coined value (spare embedding rows): PARTIAL ×2 — minted tokens land 24/24 and transfer 39–46/72, above the multi-token string (11/72) and the real-implausible rung (25/72), well below A1 (68–72/72)

_Result 2026-10-05. Decision-ID D-C10l-mint ⟨D-C10l-mint@a4a6f4c7⟩. Pre-registered `docs/C10L_MINT_TOKEN_PREREG.md` (v2; amendment B1 in §10 with its own Codex gpt-5.5 pass; implementation review before any run). Records `results/c10l_mint/` (`step0_probe.json`, `inits/{M,G,N,Z}.pt`, `tokenizer_minted/`, `arm_{multi,rare,G,N}.json`); reader `experiments/track_c/c10l_mint_read.py` (mechanical §6 labels; binding = `para_full_binding_n`); scripts `c10l_mint_lib.py`, `c10l_mint_step0.py`, `c10l_mint_arms.py` on the unmodified harness `experiments/track_c/c10e_bandknob.py` (`ARM_HOOKS` seam; engine unmodified, LAW#5 INERT every arm). LAW#3 reference: D-C10l-covgeom ⟨D-C10l-covgeom@5b553688⟩ run 1 arm A. Reviews: `results/c10l_mint/advisor_impl.md`, `advisor_b1.md`, `advisor_verdict.md`._

## Claim class
**Pre-registered falsifier (span vs novelty) on the program's C10 harness — Qwen2.5-3B fp16 MPS, band 4–8, N = 24, one seed, 24 minted tokens in the 271 spare rows of the tied embedding (no resize). A scoped PARTIAL characterisation: not a SPAN result, not route viability, not evidence that initialisation quality helps. The minted token is a Git/.vindex artefact under D-C10k-rulings-1 ruling 3.**

## VERDICT — PARTIAL ×2 (A7-mint-G 39/72, A7-mint-N 46/72), §6 sub-read G ≈ N; A1-rare 25/72; P4 (GGUF) withheld by the frozen rule

In this N = 24, one-seed harness, the admitted minted-token arms improve over the multi-token string and exceed the real-implausible rung, but remain far below A1; G did not beat N, so a row-content or grounding benefit is not shown. Exact counts (binding = post-write top-1 id at the value slot minus step-0 recall, which was 0/72 for every init):

| arm | value | canon /24 | held-out /72 | string | sibling | cannibal post | L1 /12 | described_as | L3 /30 | §6 |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 (in the G run / N run) | real plausible single token | 24 | 68 / 72 | = | — | — | 0 | 90–91 | 30 | control |
| A1-rare | real single token, BPE-id rarity proxy | 24 | 25 | 25 | — | — | 0 | 88.7 | 30 | ladder rung |
| A7-multi | coined 4–7-token string | 8 | 11 | 11 | — | — | 0 | 89.7 | 30 | baseline, inside [11, 18] |
| **A7-mint-G** | minted token, all-but-the-top init (rank 10.7) | 24 | **39** | 39 | 0 | 0 | 0 | 92.8 | 30 | **PARTIAL** |
| **A7-mint-N** | minted token, random matched-norm init (rank 23.7) | 24 | **46** | 46 | 0 | 0 | 0 | 92.2 | 30 | **PARTIAL** |

Gates: fingerprint d941a9fb inside step 0; P2 registration inert (233/233 harness prompt tokenisations unchanged; `tok(" " + value) == [ĥ]` 24/24; in-context 24/24); P3 per init (B1): M 0/24 and Z 0/24 → excluded, G 24/24, N 24/24; no cannibal or live token in any init; A1 ≥ 68/72 in every run; LAW#5 |Δexpr| ≤ 0.0005. The decoded minted id renders the coined string, so the string readout equals the binding count.

**Step 0 (no write):** P-iv on this model — M (mean of constituents) effective rank 8.7 against a 19.7 random-base-row reference, cosine mean 0.23, and `compute_z` cannot reach 0.98 on any of its 24 rows; Z: the 271 spare rows are identical vectors (rank 1.0), equally untargetable; G (all-but-the-top, k = 20, mean not added back) rank 10.7, still under the 0.75× bar yet targetable 24/24; N rank 23.7. I-11: every admitted token was dead or free before the write (0/72 step-0 recall, nothing shadowed).

**A7-multi per position (teacher-forced, held-out):** 59, 66, 51, 19, 34, 20 of 72, 72, 72, 72, 69, 39 — the drop is at the fourth token, roughly where the second coined word begins.

## Findings (scoped: Qwen2.5-3B, fp16 MPS, band 4–8, N = 24, one seed, 24 fictional subjects × 3 held-out paraphrases)

- **F-M1 (EVIDENCE-SHOWS).** Writing a coined value as one minted token lands on every canonical prompt (24/24 vs 8/24 for the string) and transfers to held-out paraphrases 39–46/72 (vs 11/72), with no sibling confusion, no cannibalism, L1 0/12, L3 30/30 and `described_as` 92. Both arms read PARTIAL: ≥ 30/72 but more than 5/72 below A1.
- **F-M2 (EVIDENCE-SHOWS, scoped).** In this run a real single token chosen by the BPE-id rarity proxy transfers 25/72 while the minted arms transfer 39–46/72; the rarity proxy is not a pure implausibility manipulation, so this is an observation about the ladder, not a general claim.
- **F-M3 (EVIDENCE-SHOWS).** G did not beat N: the random matched-norm row did at least as well as the all-but-the-top row (46 vs 39; the difference is within the per-process spread seen on this harness). P-iv is confirmed as an admission diagnostic (M and Z cannot be targeted by `compute_z`), not as evidence that a better-grounded row improves the write.
- **F-M4 (I-INFER).** The span accounts for a large part of the C10 gap but not all of it: removing it lifts transfer from 11 to 39–46/72, and the residual gap to A1 (68–72) is, by the prereg's G ≈ N branch, the novel key→value pair rather than the row. Hypotheses for the register: H-C10l-pair-novelty (instrument: I-4 knowledge spectrum / I-4b perplexingness on the per-subject hits); H-C10l-gguf (the minted row survives convert + Q4_K_M and `llama-server` tokenises the coined string — the P4 check, which the frozen rule withholds at G ≈ N and which needs an amendment or an operator deployment check).

## What this changes

- Option (iv) is a **live partial lead with a residual wall**, the first coined-value arm above 30/72 on this harness; it is not a route closure. C10 stays OPEN/BLOCKING.
- Next, in order: a P4 amendment or operator deployment check (GGUF/Q4_K_M survival of the minted row; the deployment question of ruling 3); a second seed or a second random N init for G-vs-N and minted-vs-rare (the advisor's cheapest overturning tests); lifecycle of a minted token (delete / overwrite / compaction, C5/C9) and capacity beyond the 271 spare rows; the (i) predictors on the residual gap.
- Harness facts, durable: the 271 spare rows of Qwen2.5-3B's embedding are identical vectors (init Z unusable); a mean-of-constituents row cannot be targeted by `compute_z` (P3 0/24); registration of 24 added tokens with a leading space leaves every other harness prompt's tokenisation unchanged.
- Not written here, by the advisor's instruction: "the span is the wall"; "minting solves C10"; "N is better than G"; "implausibility alone explains the gap"; "trained init is ruled out"; any change to the F1 C10 status.
- Limitations: one seed, N = 24, one model (D-C10k-rulings-2), fp16 MPS; 7/72 differences are within the per-process spread; A1-rare is a proxy rung.

## Addendum 2026-10-05 — amendments B2 (P4 GGUF) and B3 (second seed), ruling D-C10l-rulings-1: compiled-artefact gate PASS; both directional sub-reads UNSUPPORTED; PARTIAL reproduced in every replicate

_Pre-registered in `docs/C10L_MINT_TOKEN_PREREG.md` §10 B2/B3 (rules frozen before the runs; advisor pass `results/c10l_mint/advisor_b2b3.md`); this addendum reviewed by Codex gpt-5.5 (`results/c10l_mint/advisor_b2b3_verdict.md`, PROCEED with wording tightened). Records: `results/c10l_mint/step0_probe_seed1.json`, `inits/N_seed1.pt`, `arm_N_p4.json`, `arm_G_rep.json`, `arm_N_seed1.json`, `arm_rare_rep.json`, `p4_pred_f16.json`, `p4_pred_q4km.json`, `p4_verdict.json`, `p4_gguf_sha256.txt`, `logs_b2b3_chain.log`; mechanical reader `experiments/track_c/c10l_mint_b3_read.py`; P4 chain `tools/c10l_mint_p4.sh` with `c10l_mint_p4_probe.py` / `c10l_mint_p4_verdict.py`. Engine unmodified (fingerprint d941a9fb inside step 0; LAW#5 |Δexpr| ≤ 0.0002 in every arm). Edited fp16 model and both GGUFs live beside the B3 artefacts in the main checkout (`c10l_mint_edited_qwen3b_N/`, 5.9 GB; `c10l_mint_N_f16.gguf` 6.18 GB; `c10l_mint_N_q4km.gguf` 1.93 GB)._

**Step 0, seed 1 (init N only):** P2a 233/233, P2b 24/24; tokenizer SHAs, minted ids 151665–151688 and the A1-rare list identical to the original step 0. N(seed 1): effective rank 23.72 (reference 19.66), cos_mean −0.0008, step-0 recall 0/72, canon 0/24, all 24 tokens dead (0 cannibal, 0 live), P3 `compute_z` 24/24 → admitted.

**Replication (B3).** Binding = post-write top-1 id minus step-0 recall (0/72 for both inits). Every arm valid under the §6 gates.

| arm | step 0 | binding /72 | canon /24 | string | sibling | cannibal | L1 /12 | described_as | L3 /30 | A1 same run |
|---|---|---|---|---|---|---|---|---|---|---|
| A7-mint-G (original, above) | orig | 39 | 24 | 39 | 0 | 0 | 0 | 92.8 | 30 | 68 |
| A7-mint-N seed 0 (original, above) | orig | 46 | 24 | 46 | 0 | 0 | 0 | 92.2 | 30 | 72 |
| A7-mint-N seed 0, fourth replicate (P4 input) | orig | 42 | 24 | 42 | 0 | 0 | 0 | 93.5 | 30 | 69 |
| A7-mint-G replicate (fresh process, same `inits/G.pt`) | orig | 38 | 24 | 38 | 0 | 0 | 0 | 92.5 | 30 | 70 |
| A7-mint-N seed 1 | seed 1 | 34 | 24 | 34 | 0 | 0 | 0 | 90.8 | 30 | 69 |
| A1-rare (original, above) | — | 25 | 24 | 25 | — | — | 0 | 88.7 | 30 | 72 |
| A1-rare replicate | — | 29 | 24 | 29 | — | — | 0 | 89.9 | 30 | 69 |

- **Rule 1, G-vs-N ordering (supported only if N − G ≥ 5/72 in both replicates): UNSUPPORTED.** Replicate 1 (seed-0 N vs G) +7; replicate 2 (seed-1 N vs G replicate) **−4**, a sign flip. The seed-0 fourth replicate against the G replicate is +4, also under the bar.
- **Rule 2, minted-vs-rare (supported only if min(mint) − max(rare) ≥ 10/72): UNSUPPORTED.** 34 − 29 = **5**.
- **What is reproduced:** the §6 PARTIAL label holds in all five mint replicates (34–46/72: each ≥ 30 and more than 5 below its A1, locality clean on every axis), and every mint replicate exceeds every rare replicate pairwise. Spread observed: N seed 0 across processes 46 / 42; G 39 / 38; A1-rare 25 / 29; N across seeds 42–46 vs 34 — the ±5/72 per-process envelope is respected within a configuration and exceeded (12) between the two N seeds.

**Deployment (B2 / P4) — compiled-artefact gate PASS on both binding gates.**

| | fp16 GGUF | Q4_K_M GGUF |
|---|---|---|
| `/tokenize(" " + coined)` = the single minted id | 24/24 | 24/24 |
| HF-fp16 ↔ GGUF top-1 id parity — canon / para / L1 / L3 / unrelated | 24/24 / 72/72 / 12/12 / 30/30 / 10/10 | 24/24 / 43/72 / 12/12 / 30/30 / 10/10 |
| minted id top-1 — canon / para | 24 / 42 | 24 / 34 |
| failure signatures, para | none 72 | none 43, generation-id 29, string-only 0 |
| L1 prompts flipped to a minted id | 0 | 0 |
| CORPUS/17 retention (of GGUF-fp16-correct, still correct in Q4_K_M) | — | canon 24/24 = **1.000**; para 31/42 = **0.738** (3 prompts newly correct) |

The 29 Q4 paraphrase id changes fall 12 / 8 / 9 across the three held-out templates. CORPUS/17's figures (edited 99/99, native 75/77, with the top-1-margin caveat) were measured on real single-token batch edits near saturation; the minted arm sits at 42/72 with no margin measurement here, so the two retention numbers are not like-for-like.

### Findings (same scope as above; five mint replicates from three configurations, two rare replicates, one model, N = 24)

- **F-M5 (EVIDENCE-SHOWS).** Both directional sub-reads of this entry are unsupported under their pre-registered rules. F-M3 is restated: **no robust G-vs-N ordering or init-quality benefit is shown** — the two N seeds straddle the G replicates (34 and 42–46 against 38–39). F-M2's ladder observation stands with its margin stated honestly: the minted arms exceed the real-implausible rung in every replicate by 5–21/72, under the 10/72 the rule required for "supported".
- **F-M6 (EVIDENCE-SHOWS, deployment).** The minted vocabulary rows survive `convert_hf_to_gguf` and `llama-quantize Q4_K_M` as single ids in both GGUFs; the fp16 GGUF reproduces the HF edit's top-1 id on all 148 probed prompts; Q4_K_M keeps every canonical hit and 31/42 paraphrase hits with locality intact on L1, L3 and the unrelated prompts. This is **compiled-GGUF artefact viability for the minted-token representation** on this probe set: the fp16 GGUF is faithful, Q4_K_M trades size for about a quarter of the held-out paraphrase recall. It is not E1 ingest, not a product deployment loop, not native parity, and not a statement about Q4 safety in general. H-C10l-gguf is answered.
- **F-M7 (I-INFER).** The residual gap to A1 varies with the N seed (34 vs 42–46 for the same recipe). That is consistent with the prereg's "novel pair" branch read as pair-level fragility, and equally with the random row's geometry mattering; a third N seed is the live falsifier that separates seed spread from a seed effect (not in the ruling; not run).
- **Method facts.** `torch.pca_lowrank` is unseeded, so the G top-directions SHA differs between step-0 processes; the saved `inits/G.pt` tensor (hash-checked by the arms driver) is the artefact, not the recipe. The edited fp16 save is 5.9 GB. The P4 chain (convert, quantize, two server probes, verdict) takes ≈ 2 min on the M3 Pro.

### What this changes

- The verdict line above stands as **PARTIAL ×2**, now reproduced in every replicate; its two directional sub-reads ("N ≥ G", "mint ≫ rare") are withdrawn as unsupported. C10 stays OPEN/BLOCKING.
- The deployment question of ruling 3 is answered for the compiled artefact: a minted token is a Git/.vindex-ownable row that survives the compile; the operator's size-vs-recall choice (B2) is fp16 GGUF (faithful) or Q4_K_M (0.738 paraphrase retention here).
- Queue unchanged: lead 1 of the INBOX review (gold-first-token read) with the covgeom F-A5 edit + inject diagnostic; then the mint z-layer arm, the (i) predictors, lifecycle (C5/C9) and capacity beyond 271 rows. A third N seed is logged as the cheapest overturning test for F-M7.
- Not written here, by the advisor's instruction: "deployment-viable" without the compiled-artefact scope; "N is better than G"; "the minted token beats the rare rung by ≥ 10"; "Q4_K_M is unsafe for minted edits"; "Q4 degrades minted edits more than native knowledge" (no native control); "deployment loop closed"; any change to the F1 C10 status.
