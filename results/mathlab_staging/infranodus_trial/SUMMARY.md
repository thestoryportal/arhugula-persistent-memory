# InfraNodus trial — C10 verdict corpus (2026-10-08)

Input: c10_verdicts_extract.txt condensed to 25 finding statements (CORPUS/35–58 verdicts, tables and hashes stripped), sent via mcp__infranodus__generate_research_questions (useSeveralGaps). Graph not saved by name (inline text). Modularity 0.53, 8 clusters.

Gaps returned: (1) Prompt Transfer ↔ Layer Rescue; (2) Model Editing ↔ Recall Selection (oracle/adapter/ceiling); (3) Prompt Transfer ↔ Model Editing.

## Classification of the three generated questions
- Q1 "subject-keyed injection vs weight edits; can joint multi-phrase target solving rescue transfer without locality cost" — ALREADY-KNOWN: injection vs write is CORPUS/44 F-A3 and 46 F-D1; joint multi-phrase target is CORPUS/51 (UNDERFIT, write arm not run) and 52.
- Q2 "oracle-guided selection exposes whether transfer is limited by key-placement geometry rather than target solvability" — ALREADY-KNOWN as worded (key-placement axis: CORPUS/42 F6, 43 F-A1/F-A2; target solvable: 44 F-A3). But see NEW-1: the gap it sits on is real.
- Q3 "key placement mediates the injection/write gap; minted tokens transfer while multi-token fail" — ALREADY-KNOWN: CORPUS/42 F3/F6, 44 F-A3, 45 F-M1.

## NEW + TESTABLE (derived from Gap 2, sharpened by reading the files)
NEW-1. Compare the ceiling oracle's trained rank-16 update (70/72 held-out, CORPUS/57) with the closed-form update (9–16/72) on the same band 4–8: where does the adapter's ΔW put its energy relative to the covariance eigenbasis C (the directions the ridge solve suppresses), what is its effective rank per layer, and how does it respond to keys at the subject's last token inside paraphrases vs canonical prompts. A7_shuf adapters give a specificity contrast.
- Evidence it is not already addressed: grep of CORPUS/*.md and docs/*.md for adapter ΔW compared with the closed-form / key geometry / subspace returns no analysis (only GRACE spec text and LABVIZ field docs). CORPUS/57 reads behaviour and locality only.
- Inputs exist: results/c10w_oracle/p1_20261007T223707_598959Z/adapters/*_s0_r16.safetensors (A1, A2, A7_canon, A7_coined_coined, A7_shuf); Qwen covariance caches for layers 4–8.
- OFFLINE: the adapter-vs-covariance spectrum part runs now on CPU (no harvest). The comparison with the closed-form ΔW and the paraphrase-key response need the math lab's step-1 harvest.

Counts: ALREADY-KNOWN 3, NEW+TESTABLE 1 (from a gap, not from a generated question verbatim), NOISE 0.
Verdict: TRIAL USEFUL — modestly. The generated questions restated known results; the gap structure pointed at one unexamined link (the trained ceiling update's geometry), which is offline-testable on files we already have.
