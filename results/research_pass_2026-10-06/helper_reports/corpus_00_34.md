# CORPUS/00–34 (helper read in full; condensed)

## Verdict lines bearing on this pass
- 04 ENV: covariance compute "~11–17 min/layer × 5 = ~70 min" on the RunPod 4090 (04:33); 3B `lm_head=embed_tokens tied` (04:25); Gemma not used (04:28).
- 09 CP3: `rewrite_module = mlp.down_proj` (09:18); `mom2_dataset = wikipedia` (09:19); band [4–8] sits at ~11–22 % depth on 3B vs the spec's C15 ~47–78 % (09:55–56); the solve `A = Pi·(K Kᵀ + cache_c) + L2·I`, projector from `svd(cov)` (09:13–15).
- 13 G6.1 / 14 A1: sequential held-out top-1 100→41.7 % at N=100; batch stays 100 % (13:28, 14:19–20) → batch (Genesis) path is the clean path.
- 16 A2b: BetaEdit config recorded as "band[4-8]/`mlp.down_proj`/`subject_last`/wikipedia" (16:39); A3 port parked.
- 17 B3: Q4_K_M retention edited 100 % vs native 97.4 % (17:21–23).
- 18 E1: LARQL cannot serve Qwen2.5 (attention-bias drop; A7 causal); llama.cpp adopted (18:54).
- 19 B1: Qwen2.5-7B "28L, hidden 3584" (19:11), intermediate 18944 (22:70); 18944-dim SVD moved to CPU; batch 91.7 % (19:20).
- 20 C2: relation-key cosine 0.93–0.94 vs subject-key 0.26–0.68; minimum at L8–12 (20:14–25).
- 22 D1: concentration law model-general; guardrail k≤1 (00:154 etc.).
- 23 D20 / 26 C1-KVC: sub-batched compaction reintroduces corruption only as a scale × sub-batching interaction (26:18–21).
- 27 R2: forward edit creates zero reverse edge (27:21) → reverse lookup side-store-delegated.
- 28 R13 / 29 R5 / 30 R5b: trained prompt 100 % → ~22 % paraphrase for counterfactual-over-prior; novel facts 16/16 robust; the axis is pretrained-prior presence (28:18, 29:14–17, 30:17).
- 31/32 R1: in-weight logprob storage signature bleed-unsound; commit-bit SELECT delivered for commit time.
- Nothing in 04–34 is primarily about multi-token values; that chain is 35–50.

## F1 conditions named across 00–34
C1 compaction/scale (pressured, not falsified); C2 read contract (post-commit divergence open); C3/R5 native-knowing robust iff no entrenched pretrained competitor; C5 compaction verify (prototyped); C6 ledger (open); C8 constraint read; **C10 multi-token values — "OPEN MUST-FIX … the FIRST condition both on the critical path AND failing" (00:188), OPEN/BLOCKING at the latest entries (00:251, 03:129)**. No enumerated F1 list lives in CORPUS; it is in `docs/F1_DETERMINATION.md`.

## Rulings' exact wording
- D-C10k-rulings-1 appears in CORPUS only as "strict held-out-paraphrase full-sequence bar binds" (49:3, 50:3) and "minted token is a Git/.vindex artefact under ruling 3" (45:6). The full text is runbook row 307 (read directly by the lead).
- "RB:305" is a runbook row (D-B3N-1), not a CORPUS line; CORPUS carries only "already side-store-routed" (00:179) and "reverse leg entirely side-store-delegated" (00:203).

## Model-family facts
GPT-J-6B eliminated (same-entity locality 67.98 %, 00:17); Qwen2.5-7B clean single edit 99.86 % (00:18), batch 91.7 %; Qwen2.5-3B hparams band [4–8], v_loss 35, mom2_update_weight 5000, tied, 36 layers, 108 q/k/v biases; Qwen3-0.6B serve model (28L, 3072² covariances, L4 654 s … L8 1006 s on the pod, 01:25); Qwen3-4B planned then replaced by 7B (03:66); Gemma licence-gated; **no M3 Pro wall-clock timings for covariance or edits anywhere in 00–34**; MPS recommended ceiling 37.4 GB (00:224).

## External methods named in 00–34
kmeng01/memit (engine), AlphaEdit (adopted), ROME/GRACE/FT (excluded by D12), BetaEdit (A3, parked), SAE basis change (named), AnyEdit (pilot + port halted), AnyEdit++/μKE (un-falsified), Hernandez LRE (mechanism), RoSE/IGA P := I (NULL), OverTone I-1 / forward replay I-2 (next), Moir (untested), LARQL (serve falsified for Qwen2.5), llama.cpp (adopted). Not mentioned: PMET, EMMET, WISE, MEND, any non-Qwen model besides GPT-J and Gemma.
