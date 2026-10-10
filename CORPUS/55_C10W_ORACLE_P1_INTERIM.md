# 55 — Ceiling oracle (step 5), P1 only: INTERIM seed-0 reading; the reader returns INCOMPLETE (no label, no routing)

**ORACLE MEASUREMENT — not a route; never promotable as a write-engine result**

_Interim record 2026-10-07 UTC. Decision-ID D-C10w-oracle. ⟨D-C10w-oracle@64bf1ecd⟩ Pre-registration docs/C10W_ORACLE_PREREG.md v2.2 FROZEN + Amendment A-dupdev (§9), sha256 d2aa240e… (equal to the pinned reader's PREREG_SHA, experiments/track_c/c10w_oracle_read.py:20). Phase P1 only, directory results/c10w_oracle/p1_20261007T223707_598959Z/ (below `P/`); step 0 results/c10w_oracle/step0_20261007T223638_531381Z/. Pinned reader experiments/track_c/c10w_oracle_read.py sha256 16296611… (equal to the step-0 pin). Binding reader output P/verdict.json: status INCOMPLETE, final_label null, routing null (:4–6). Interim configuration record P/interim_reader_configuration_v2.json (class line, Decision-ID, producer experiments/track_c/c10w_oracle_interim.py sha256 3d46fdb9…, reader sha256 16296611…, P/eval.json sha256 f8886427…); its reading equals the older P/interim_reader_configuration.json, which lacks those fields and is not the cited source. Authority: P1 approved by prereg §8 item 3 (:532) with the budget set by operator ruling D-C10r-rulings-10 (1) (runbook §5.2, EXPERIMENT_RUNBOOK.md:353; P/authorization_P1.json, 592 min). Engine unmodified, fingerprint d941a9fb/PASS (P/eval.json `fingerprint`). Verdict reviews of P1 (2026-10-07): GPT-6-Astra high results/c10w_oracle_reviews/p1_verdict_astra.md (PROCEED, all advisory); Opus advisor run 1 results/c10w_oracle_reviews/p1_verdict_advisor_run1.md (FIX-FIRST, three BLOCKING) and run 2 results/c10w_oracle_reviews/p1_verdict_advisor.md (FIX-FIRST, one BLOCKING, the same point as run 1's issue 2). Every blocking item is folded below. Lineage: CORPUS/44 ⟨D-C10l-covgeom@af2e38f7⟩, CORPUS/45 ⟨D-C10l-mint@a4a6f4c7⟩, CORPUS/54 ⟨D-C10u-mint2@d1299b2b⟩._

## Status

P1 is complete and valid. The pinned reader returns **INCOMPLETE**: no final label and no routing until P2 replicates (prereg §8 item 3, :532: "Without required replication, issue no final scientific label or routing"; replication is "required before any label routes", :370). **D-C10w-oracle stays OPEN; this entry does not close it.** **Step 5 is NOT "read" for D-C10r-rulings-10 (3)** (steps 6 and 7 go "once steps 3–5 are read", EXPERIMENT_RUNBOOK.md:353), **so steps 6–7 do not start on this entry.** C10 stays OPEN/BLOCKING; F1 is unchanged.

**Departure from the review order.** Prereg §6 places the CORPUS entry after P2, (P3) and the verdict review (:452). Writing a CORPUS entry at P1 departs from that order. This is an interim record; the final entry for D-C10w-oracle follows the post-P2 verdict review. Both reviewers permitted the interim entry on these terms (p1_verdict_astra.md item 2; p1_verdict_advisor_run1.md issue 1 and answer B; p1_verdict_advisor.md issue 3).

## What P1 measured, and validity

Step 5 trains a merged rank-16 LoRA on the five band `down_proj` matrices (layers 4–8) of Qwen2.5-3B on the 24 coined facts and scores it on the C10 harness against the same-process closed-form MEMIT write. It is an oracle beside the write path, not a write engine (prereg :3, :19–23). P1 trained five adapters at seed 0 (O-A1, O-A2, O-A7, O-A7-shuf, O-A7-canon) and evaluated three recipes (closed form, oracle, canonical-only oracle) in one process.

- All five trainings passed at 400 steps with no retry: fit 480/480 for O-A1, O-A2, O-A7 and O-A7-shuf, 24/24 for O-A7-canon; wall 6.2–8.7 min each, 37.1 min in total (P/eval.json `train_records`; p1_verdict_advisor_run1.md:20).
- P/eval.json `status` PASS, all six `validity` flags true. LAW#5 (i)–(vi) pass: (i) gives |Δexpr| 0.0004 and Δloc 0.27 in every recipe, but (i) exercises the delegation path, so it shows the seam delegates inertly and does not test the oracle application; that is covered by (ii) the zero adapter, (iii) restore (band hash after = base in every recipe), (v) hits 1/1 and 5/5, and (vi) the seam check in step 0 (p1_verdict_advisor_run1.md issue 7).
- LAW#3: closed-form A7 9/72 held-out full-sequence, first token 52/72, canonical 9/24, inside the envelope; closed-form A1 72/72, A2 70/72; arm U A7 0/72, stimulus base 0. Trainer positive controls O-A1 72/72 and O-A2 72/72 (P/eval.json `recipes.closedform.arms`, `recipes.oracle_p1.arms`, `u`).
- P1 evaluation wall time 96.2 min (P/eval.json `wall_seconds` 5773.7), not ~95; preflight 59.8 min.

## Interim seed-0 configuration (non-routing; not the result)

From the pinned reader's own `configuration()` applied to P1 (P/interim_reader_configuration_v2.json `oracle_p1_A7_configuration`). This is a single-seed per-configuration reading (§3, :359–365): interim, non-routing, not replicated, and not a final label. The experiment's status is INCOMPLETE, and no sentence here says the measurement "is" this label.

| Readout (rank 16, seed 0) | Value | Source |
|---|---|---|
| O-A7 held-out full-sequence | **70/72** (mounted 70; first token 72/72) | `count`, `mounted_count`; eval `para_first_n` |
| Same-process closed-form A7 | 9/72 | eval `recipes.closedform.arms.A7_coined_coined.para_full_n` |
| Per template Q1 / Q2 / Q3 | 22 / 24 / 24 | `per_template_counts` |
| Facts passing all three templates | 22/24 (misses Zorbland and Plurnak, both on Q1, first token right) | `per_edge_pass`; p1_verdict_advisor_run1.md:79 |
| Gates | G1, G2, G3, G5, G7 pass; **G4 MISS**; G6 passes exactly at its limit | `gates` |
| Configuration label | **PARTIAL-CEILING-LOCALITY-COST(G4)**, qualifier **BIGRAM** | `label`, `qualifiers` |

**G4 (same-frame locality).** The rule needs the canonical frame and each of the 20 training frames to stay within the closed form's flips + 1, of 6 never-edited fictional subjects (prereg :354). The canonical frame passes, 1/6 against 1/6. Fifteen of the 20 training frames miss (T02, T03, T06–T12, T14, T16–T20; T08 is 5/6 against 0/6). Summed over the training frames the oracle has 50/120 against the closed form's 4/120 (P/eval.json `recipes.*.arms.A7_coined_coined.extra.frames.train[*].flips`). A flip means a never-edited fictional subject's top-1 moved into the edited values' FIRST-TOKEN set (experiments/track_c/c10w_oracle_eval.py:119–125): this counts first-token membership, not full-value retrieval. The frames are compared one by one; they are not pooled into one denominator (p1_verdict_astra.md item 3).

**G6 (MMLU-200).** Net paired loss against U is 4/200 (13 correct→wrong, 9 wrong→correct), exactly at the limit (loss 4 passes, loss 5 misses, prereg :368). The matched shuffled control loses 9/200 and O-A2 5/200 (P/verdict.json `g6_sensitivity`, report-only).

**G7 (shuffled control).** O-A7-shuf scores 71/72 on its own map and 0/72 cross-scored against the original map, so G7 passes and PAIRING-SPECIFIC does not fire (gap |70 − 71| = 1).

**BIGRAM.** 24 facts eligible, 0 excluded; C = 24; X = 17 ≥ threshold 12 (⌈24/2⌉), so BIGRAM fires (c10w_oracle_read.py:245–255; prereg :230). Within X: the swapped subject continues with fact k's modifier after k's head for 13 facts, at least half of the six never-edited subjects do for 13 facts (mean n 0.486), and the head-sharing sibling never does (b = 0 for all 24). BIGRAM measures modifier continuation after a supplied head under off-subject conditions. It does not show that the successes were caused by leakage, and it does not cancel the G7 pass (p1_verdict_astra.md item 4). The closed form gives C = 9, X = 0; O-A7-shuf and O-A7-canon are also BIGRAM (X = 13 and 15).

70/72 is attained benchmark performance of one finite recipe at one seed on this fixed, test-aware benchmark. It is not a model ceiling, not an upper bound, and not a causal explanation (prereg :23, :406). "70 against 9" is the comparison; the +61 gain is not related to the 61/72 bar.

**O-A7-canon s0 (single-frame ablation; read only through the split).** Canonical 24/24, held-out 2/72, first token 5/72. Its reader gates fail G2 (L3 12/30 < 29) and G4 (canonical frame 3 against 1; T01 3, T13 4, T15 3 against 1/1/1) (p1_verdict_advisor.md issue 1). The 24/24 against 2/72 contrast is descriptive only; it supports no claim that extra frames caused transfer (prereg :53, :394 (b)).

## What P2 can and cannot return

These follow mechanically from the P1 records and the frozen reader. They are structural consequences, not a final label (p1_verdict_advisor.md issue 1; p1_verdict_advisor_run1.md issue 2).

- **No rank-16 PASS-CEILING is possible.** The replicated label takes the union of both seeds' gate misses (`c10w_oracle_read.py:382`), and seed 0 already misses G4 on 15 of 20 frames.
- **The canonical split will be NOT-READ (case c).** The split needs G1–G6 to hold at both seeds (`read.py:403`; prereg :388), and O-A7-canon s0 already fails G2 and G4. Its 24/24 against 2/72 stays descriptive whatever P2 shows.
- **Likely end state:** PARTIAL-CEILING-LOCALITY-COST(G4) with no reference count: reference_count null, reference_status NO-GATE-CLEAN-REFERENCE (`read.py:461–464`; prereg :395). Steps 6–7 would then proceed only on their own rationale.
- **Real -UNSTABLE risk.** G6 sits at its limit (4/200), and the shuffled control loses 9/200. If the same-seed retrain changes any binding gate's pass/fail result, for example G6 at a loss of 5, the reading is -UNSTABLE: no label, no routing, no P3 (prereg :370; `read.py:390`).
- **P3 (rank 64) is the only route to PASS-CEILING or a gate-clean reference,** and it runs only if the replicated rank-16 label is a stable PARTIAL-CEILING or FAIL-CEILING, never after LOCALITY-COST or -UNSTABLE (prereg :372). With s0 = 70 and G4 already in the union, the realistic trigger is a narrow window: seed 1 at about 55–60, with the retrain still ≥ 61, within 10 of 70 and with identical gates. Seed 1 ≤ 54 gives a seed gap > 15 (-UNSTABLE); seed 1 ≥ 61 gives LOCALITY-COST, which excludes P3 (p1_verdict_advisor.md issue 6 (d)). P/verdict.json `"p3_required": false` is the default for an INCOMPLETE reading, not a determination.

**Projections** (P/verdict.json `projection`): P2 178.0 min against an allowance of 448; P3 138.3 min against 327. The P3 figure is a rank-16-based projection (`c10w_oracle_step0.py:347` reads it at P3 entry; `rank64_training_timing`: "rank16 projection; remeasure each rank64 attempt") and is not re-projected after P2. Estimates below an allowance do not authorize anything (prereg :532).

## Advisories carried (ungated readouts; none changes the reading)

- **Large ungated distributional locality shift.** O-A7 L3 mean KL 1.066 against the closed form's 0.00013, with L3 top-1 still 30/30; L1 / L3 JS locality 87.66 / 89.19 % against 100.0 / 100.0; generic perplexity falls 21.755 → 21.081 (G5 is one-sided, so a fall passes). Locality is not "otherwise clean" (P/eval.json `recipes.oracle_p1.arms.A7_coined_coined.locality_axes`; p1_verdict_advisor_run1.md issue 4).
- **G4 flips are mostly single-letter first tokens.** The oracle's 50 training-frame flips are ' V' 30, ' D' 17, ' K' 3; the closed form's 4 are ' V' 3, ' Vor' 1. Held-out frames 2/2/2 against 0/0/0 (report-only). The O-A1 positive control shows the same pattern (canonical 6/6, training frames 3–6/6), so the pull toward trained first tokens in trained frames is a property of the recipe, not of A7 (P/eval.json `extra.frames`; p1_verdict_advisor_run1.md:99; p1_verdict_advisor.md issue 5).
- **Relation probes (report-only).** "is a" flips on 23/24 edited subjects for O-A7; the closed form also flips 23/24, so this probe does not separate the two. "is associated with" flips 12/24 against 5/24 (P/eval.json `extra.relations`; p1_verdict_advisor.md issue 5).
- **Canonical adapter damage to the real-country frame.** O-A7-canon s0: L1 top-1 changed 6/12 (none to an edited value), L3 12/30, KL 3.185, JS 42.52 / 39.31 %. Report its 2/72 only together with this damage (P/eval.json `recipes.oracle_canon_s0.arms.A7_canon.locality_axes`; p1_verdict_advisor_run1.md issue 6).
- **Closed-form null-cov share above 1.** The closed form's `null_cov_share` is 1.0039–1.0122 across layers 4–8, where 1.000 is expected (prereg :225), so P is not an exact projector at this precision or ΔW is an fp16 difference. The oracle's shares (0.73 at layer 4 down to 0.10 at layer 8) are not fractions against an exact 1.000 baseline. Write-size ratio oracle / closed form 0.319 (P/eval.json `extra.geometry`; p1_verdict_advisor_run1.md issue 8).

## Not claimed

Not a final label, not a routing, and not "step 5 read". Not a ceiling or upper bound on this model or on other writers, and not evidence that a missing objective is the cause (prereg :406). Not a write-engine result or a route; training is outside the spec's write path (prereg :3, spec :313). Not a claim that 22/24 per-edge or 70/72 means universal read correctness, that locality is clean, or that the successes are subject-bound beyond what G7 tests. Not a causal claim about frame diversity from O-A7-canon. Not a generalisation beyond this test-aware benchmark (prereg :407). No CORPUS/37–54 label changes; the 61/72 program bar is not reached by a replicated reading; C10 remains OPEN/BLOCKING and F1 is unchanged.

## Decision-ID and FORK

D-C10w-oracle: OPEN. P1 complete and valid; reader status INCOMPLETE; interim, non-routing seed-0 configuration reading PARTIAL-CEILING-LOCALITY-COST(G4) with BIGRAM at 70/72 against the closed form's 9/72. This entry does not close the D-ID, and step 5 is not read.

Next: the operator's authorization question, in plain words. P2 (the repeat run: seed 1, a same-seed retrain, and the matched controls) costs up to 448 min against a projected 178. Under the frozen rules it can return a replicated LOCALITY-COST or PARTIAL label, an -UNSTABLE diagnosis, or eligibility for P3; it cannot return a rank-16 PASS-CEILING or a readable canonical split. Conditional P3 (rank 64) costs up to 327 min against a rank-16-based projection of 138, runs only if the rules call for it (the narrow window above), and would start with no further check-in; asking about P3 after P2 is the conservative alternative. The program may not write `authorization_P2.json` without the operator's yes. The final CORPUS entry for D-C10w-oracle follows P2, (P3) and the post-P2 verdict review.

Overturning test (both reviewers): P2 itself, the seed-1 count against s0 and the same-seed retrain against G6 at its limit and G4. No cheaper model-free control remains; the artifact-level recomputation of counts, frame indicators and reader output already passed (p1_verdict_astra.md item 7).

_Verdict sentence merged from the GPT-6-Astra and advisor P1 reviews (p1_verdict_astra.md "Proposed CORPUS/55 verdict"; p1_verdict_advisor_run1.md:198–200; p1_verdict_advisor.md:109–111): ORACLE MEASUREMENT — not a route; never promotable as a write-engine result. P1 is complete and every P1 validity control passed, but D-C10w-oracle remains INCOMPLETE, with no final label or routing until P2 replicates. As an interim, non-routing seed-0 configuration reading, the rank-16 oracle scored 70/72 held-out against the same-process closed form's 9/72, missed G4 on 15 of 20 training frames, passed G6 exactly at its 4/200 limit and carries BIGRAM, i.e. PARTIAL-CEILING-LOCALITY-COST(G4); under the frozen rules rank 16 can no longer yield PASS-CEILING or a readable canonical split. C10 remains OPEN/BLOCKING and F1 is unchanged._

## Closing pointer (appended 2026-10-08; the interim text above is unchanged)

P2 replicated and the post-P2 verdict review confirmed the reading: the final entry is **CORPUS/57** ⟨D-C10w-oracle@6a735469⟩ — PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM; replicated 70/72; P3 not required; canonical split NOT-READ; NO-GATE-CLEAN-REFERENCE; routing INDEPENDENT-PREREG-ONLY. D-C10w-oracle is CLOSED there; this interim record is history, not the cited source.


⟨D-C10l-covgeom@0caeca4f⟩
