# Hypotheses — research pass 2026-10-06 (D-C10r-rulings-2)

Leads, never evidence. Nothing here was run. Every arXiv id, repository and checkpoint named below was opened in this pass or is carried from the inventory's already-verified list (marked *inv*). The bar is the program's: held-out full-sequence recall of the coined value on 24 subjects × 3 unseen paraphrases (out of 72), with locality scored on the separate axes of CORPUS/44 (L1 real-country flips out of 12, `described_as` JS, L3 unedited-capital top-1 out of 30, same-frame fictional probe out of 6, generic perplexity). A source's "generalization" on CounterFact or zsRE is not that bar and is labelled so in each entry.

## Conventions used in every entry

- **class**: the plan's §1a taxonomy (E1–E9, M1–M5).
- **cheapest test**: what would run on this Mac (M3 Pro, 48 GB, MPS), on which arms, how long, with pre-registerable numbers. Shared thresholds taken from the harness after CORPUS/44–50: identical-baseline envelope for A7 `para_full` [5, 18]/72 and canon [5, 10]/24; LEAD ≥ 30/72; PARTIAL or TRADEOFF needs a gain ≥ 10/72 over the same-run baseline; route bar ≥ 61/72 (85 %); controls A1 and A2 ≥ 68/72; locality gates L1 ≤ baseline + 1, `described_as` ≥ baseline − 3, L3 ≥ 29/30, same-frame ≤ baseline + 1, perplexity rise ≤ 0.5; write-size qualifier ΔW ratio ≤ 1.5× the single edit (CORPUS/50). Timing anchors: one full harness pass (A1 + A2 + A7, N = 24, band 4–8) ≈ 33 min (CORPUS/50: three passes in 02:15–03:54); one injection cell ≈ 40 min (CORPUS/47); the GGUF chain ≈ 2 min (CORPUS/45). Covariance for a new model band took about 70 min on the lost 4090 (CORPUS/04:33); no M3 Pro timing exists, so every model-change test carries "covariance time unmeasured".
- **would-advance**: the F1 condition or spec obligation moved. C10 is the OPEN/BLOCKING multi-token value condition; §C is the write path; §F / §8.9 is the L2 behavioural probe; Part V open questions are OQ-W1 (thresholds) and OQ-W2 (MEMIT / architecture compatibility).
- **spec-amendment**: none, or the section that would change. A continued-pretraining or fine-tuning route replaces the §8.2 D12 write engine and the entry says so.
- **feasibility**: `static` (prefilter arithmetic only) or `empirical` (an existing run on this Mac, cited). The prefilter uses the edited matrix: the harness edits `down_proj`, whose input dimension is the MLP intermediate size, so one fp32 covariance or projector is intermediate² × 4 bytes (Qwen2.5-7B: 18,944² ≈ 1.34 GiB each, CORPUS/41; Qwen2.5-3B: 11,008² ≈ 462 MiB).
- **source-metric**: what the source reports and its distance from our bar.
- **disposition**: `candidate` / `candidate-needs-C10-eval` / `lead` / `fallback` / `empty` as the plan's §4 defines them. This pass runs nothing, so a new model is at most `lead`.

Entries are grouped by class. H-numbers are stable; the ledger nodes in the OpenResearch project carry the same numbers.
