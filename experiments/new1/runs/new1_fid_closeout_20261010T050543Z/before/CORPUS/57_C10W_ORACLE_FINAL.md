# 57 — Ceiling oracle (step 5), final replicated reading: PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM

**ORACLE MEASUREMENT — not a route; never promotable as a write-engine result**

_Final record 2026-10-08. Decision-ID D-C10w-oracle (CLOSED by this entry) ⟨D-C10w-oracle@6a735469⟩; process ruling D-C10w-p2rerun. Pre-registration docs/C10W_ORACLE_PREREG.md v2.2 FROZEN + Amendment A-dupdev (§9), sha256 d2aa240e… Interim P1 record: CORPUS/55 (kept unchanged as history; its closing pointer is appended there). P2 directory results/c10w_oracle/p2_20261008T034226_086980Z/ (below `P2/`). Binding reader output results/c10w_oracle_logs/p2-read-attempt2.json, sha256 b311c070… (byte-identical to P2/verdict.json), status **VALID**, produced by the pinned reader experiments/track_c/c10w_oracle_read.py sha256 16296611… P2 eval P2/eval.json sha256 7b00b1a5…, `status` PASS, all six `validity` flags true, wall 5955.1 s (99.25 min). Coordinator log results/c10w_oracle_logs/p2-reattempt-coordinator.20261008T030455.59886.log: DONE p2-eval 04:44:14, COORDINATOR_EXIT=0 04:44:15 MDT. Engine unmodified, fingerprint d941a9fb/PASS, `_cov_cpu` 3 (P2/eval.json `fingerprint`). Verdict review: GPT-6-Astra high, results/c10w_p2_reading_astra.md — **CONFIRM, no BLOCKING**; every number below is from that review or the reading. Lineage: CORPUS/55, CORPUS/44, CORPUS/45, CORPUS/54._

## Verdict

The replicated rank-16 reading is **PARTIAL-CEILING-LOCALITY-COST(G4,G6)**, qualifier **BIGRAM**. Replicated count min(70, 71) = **70/72** held-out (goal 61/72; same-process closed-form A7 9–16/72 across preflight, P1 and P2; gain over the closed form +61 at seed 0, +60 at seed 1). Seed 0 misses G4; seed 1 misses G4 and G6; the label carries the union (prereg §3, :329; `c10w_oracle_read.py:382`). Stable: seed gap 1 ≤ 15; same-seed retrain 70 → 70 with prompt agreement 72/72 and identical gate outcomes; no -MERGE-LOSS, no -UNSTABLE.

- **P3 not required** (`p3_required` false): P3 runs only after a replicated PARTIAL-CEILING or FAIL-CEILING and is excluded after LOCALITY-COST (prereg :372, :378). This exclusion is scope and budget policy, not evidence that a higher rank cannot improve locality.
- **Canonical split NOT-READ (case c)**: the canonical-only adapters score 2/72 (s0) and 3/72 (s1), but L3 is 12 and 17 of 30 against ≥ 29, and canonical-frame flips are 3 and 4 against ≤ 2, so G1–G6 do not hold at both seeds (prereg :388).
- **No gate-clean reference**: no completed rank passes every gate at both seeds → `reference_count` null, `reference_status` NO-GATE-CLEAN-REFERENCE (prereg :395).
- **Routing INDEPENDENT-PREREG-ONLY** (`routing.action`; `h30_eligible` false, `mechanism_attribution` false): steps 6–7 proceed only on their own preregistered rationale; no reference count is passed to them and no costly count substitutes for one. C10 stays OPEN/BLOCKING; F1 is unchanged.

**Plain meaning (reviewer's wording, kept):** this finite training recipe recalled 70 and 71 of 72 held-out reworded prompts, strong recall on this fixed benchmark. It does not establish the ≥ 61/72 goal with clean locality: G4 misses 15 of 20 training frames at each seed (including 5 flips against 1 allowed and 4 against 1), seed 1 also has 3 canonical-frame flips against 2 allowed, and the MMLU net losses are 4/200 and 6/200 against 4/200 allowed. In everyday words: training the five band `down_proj` matrices can make the model recall made-up two-word names under reworded questions at 70–71 of 72, so capacity on this band is not the wall; this recipe got there with side effects (other facts disturbed, a general-knowledge loss on one seed), so a clean ceiling is not shown.

## Gates and counts (rank 16)

| Readout | Seed 0 (P1) | Seed 1 (P2) | Same-seed retrain (P2) | Source |
|---|---|---|---|---|
| O-A7 held-out full-sequence (mounted) | 70 (70) | 71 (71) | 70 (70) | reading `ranks.16` |
| Per template Q1 / Q2 / Q3 | 22 / 24 / 24 | 23 / 24 / 24 | 22 / 24 / 24 | `per_template_counts` |
| Gain over same-process closed form | +61 | +60 | +59 | `gain_over_closedform` |
| Gate misses | G4 | G4, G6 | G4 | `gate_misses` |
| G6 MMLU-200 net paired loss vs U | 4/200 (passes at the limit) | 6/200 (misses) | 4/200 | `g6_sensitivity` |
| BIGRAM (C, X vs threshold 12) | 24, 17 | 24, 14 | — | review, Label |
| Configuration label | PARTIAL-CEILING-LOCALITY-COST | PARTIAL-CEILING-LOCALITY-COST | PARTIAL-CEILING-LOCALITY-COST | `label` |

G4 is the same-frame locality gate (a never-edited fictional subject's top-1 moving into the edited values' first-token set, per frame against the closed form's flips + 1; prereg :354; first-token membership, not full-value retrieval; CORPUS/55 §G4). G7 holds throughout: matched shuffled cross-scores 0/72. BIGRAM measures modifier continuation after a supplied head under off-subject conditions; it does not show that the successes were caused by leakage and does not cancel the G7 pass (CORPUS/55 §BIGRAM).

## Validity (all from the review)

- P1 and P2 eval: all six validity flags true. Nine full-template adapters fit 480/480, both canonical adapters 24/24, all at 400 steps; frozen-parameter hashes match. Positive controls: P1 O-A1/O-A2 72/72 each, P2 O-A1 72/72.
- LAW#3 (closed form, preflight / P1 / P2): A1, A2 = 72, 72 / 72, 70 / 71, 71; A7 full / first token / canonical = 16/54/8, 9/52/9, 11/54/7, all inside their envelopes; arm U and stimulus counts zero.
- LAW#5 standing check |Δexpr| / Δloc = 0.0017/0.04, 0.0004/0.27, 0.0002/0.91; null counts, probes and weights identical, perplexity Δ 0, described_as 100; delegation and restores pass; zero-adapter hits 1/1, trained hits 5/5 and 6/6; nonzero seam maximum errors 1.993×10⁻⁷ / 1.211×10⁻⁷ (< 10⁻⁵).
- Stability: float64 same-seed cosines 0.9999999999992969–0.9999999999994948; merged and mounted counts match throughout.
- Budget: maximum training projection 8.32 < 90 min; sampled driver memory 29.858 < 40 GB; P2 evaluation 99.25 < 240 min; P2 projection including the halted evaluation 363.07 < 448 min (`authorization_P2.json`, D-C10r-rulings-12).

## Process history (P2)

1. **Attempt 1 halted, not read (D-C10w-p2halt, runbook §5.2).** All six P2 training stages exited 0; the evaluation scored every recipe, then the reader's validity check refused the same-seed cosines 1.007–1.009 (> 1). Cause: a 22.5M-element fp32 dot-product accumulation in `c10w_oracle_eval.py`. Diagnostic `architecture_profile/s29_c10w_p2_cosine_halt_diagnostic.json`.
2. **Operator ruling D-C10w-p2rerun (2026-10-08 ~01:55 MDT):** rerun the evaluation on the GPU after a reviewed fix; a compromised run is always re-run, never read around.
3. **Evaluator amendment A1** (`results/c10w_oracle/step0_20261007T223638_531381Z/amendment_A1_evaluator.json`, sha256 4791183a…): two float64 casts in the cosine accumulation only; reviewed GO by GPT-6-Astra (`results/c10w_p2rerun_astra_review.md`). The reading and P2/eval.json both carry this SHA.
4. **Halted attempt archived** to `P2/attempt1_halted/` (manifest sha256 3b2fd266…); it supplies no scientific reading, only audit and budget provenance.
5. **Re-attempt** (`P2/reattempt2.json`): gate ok, launched 03:04:55, 99.25 min, COORDINATOR_EXIT=0 at 04:44:15 MDT.

## Not claimed

Not a write-engine result, a route or a promotable claim; training is outside the spec's write path (prereg :3; spec :313). Not a model ceiling or an upper bound on this model or other writers, not a causal explanation, and not evidence that a missing objective is the cause (prereg :23, :406). Not a clean ceiling: the locality and forgetting gates fail. Not a generalisation beyond this fixed, test-aware benchmark (prereg :407). Not evidence that rank 64 would or would not fix locality (P3 was excluded by policy). Not a claim about frame diversity (the canonical split is NOT-READ). No CORPUS/37–56 label changes; C10 remains OPEN/BLOCKING; F1 is unchanged.

## Decision-ID and next

D-C10w-oracle: **CLOSED** — PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM; replicated 70/72; P3 not required; canonical split NOT-READ; NO-GATE-CLEAN-REFERENCE; routing INDEPENDENT-PREREG-ONLY. D-C10w-p2rerun: DONE (the rerun produced this reading). Step 5 is now read for D-C10r-rulings-10 (3): steps 6 (C10X) and 7 (C10Y) proceed on their own preregistered rationale, with no reference count from this oracle. H-13 is measured (oracle); H-15 and H-30 are not run.

_Verdict sentence: ORACLE MEASUREMENT — not a route; never promotable as a write-engine result. The replicated rank-16 band-LoRA oracle recalled 70 and 71 of 72 held-out reworded prompts (closed form 9–16/72), but missed same-frame locality (G4) at both seeds and the MMLU forgetting gate (G6, 6/200) at seed 1, so the final label is PARTIAL-CEILING-LOCALITY-COST(G4,G6) with BIGRAM; P3 is excluded, the canonical split is not read, there is no gate-clean reference, and steps 6–7 proceed only on their own preregistered rationale. C10 remains OPEN/BLOCKING and F1 is unchanged._
