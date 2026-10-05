# 45 — Mint one vocabulary token per coined value (spare embedding rows): PARTIAL ×2 — minted tokens land 24/24 and transfer 39–46/72, above the multi-token string (11/72) and the real-implausible rung (25/72), well below A1 (68–72/72)

_Result 2026-10-05. Decision-ID D-C10l-mint ⟨D-C10l-mint@5fd0d6ae⟩. Pre-registered `docs/C10L_MINT_TOKEN_PREREG.md` (v2; amendment B1 in §10 with its own Codex gpt-5.5 pass; implementation review before any run). Records `results/c10l_mint/` (`step0_probe.json`, `inits/{M,G,N,Z}.pt`, `tokenizer_minted/`, `arm_{multi,rare,G,N}.json`); reader `experiments/track_c/c10l_mint_read.py` (mechanical §6 labels; binding = `para_full_binding_n`); scripts `c10l_mint_lib.py`, `c10l_mint_step0.py`, `c10l_mint_arms.py` on the unmodified harness `experiments/track_c/c10e_bandknob.py` (`ARM_HOOKS` seam; engine unmodified, LAW#5 INERT every arm). LAW#3 reference: D-C10l-covgeom ⟨D-C10l-covgeom@5b553688⟩ run 1 arm A. Reviews: `results/c10l_mint/advisor_impl.md`, `advisor_b1.md`, `advisor_verdict.md`._

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
