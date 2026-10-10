FIX-FIRST

**Next:** retain the five published rows, but correct the claim that pairing makes the duplicate harmless and explicitly pin the rerun to the inspected dataset commit.

**BLOCKING**

1. **Identical prompts do not guarantee identical effects on U and edited models.** The immunity claim in `docs/C10W_ORACLE_PREREG.md:540` is false. G6 sums \(d_i=\mathrm{correct}_U-\mathrm{correct}_O\), with each \(d_i\in\{-1,0,1\}\) (`experiments/track_c/c10w_oracle_read.py:261–267`). The two affected items contribute between −2 and +2. Changing their prompts could change net loss by **up to four counts**, enough to cross the **4-pass/5-fail** boundary. This is an arithmetic possibility, not an observed effect.

   **Replace §9 “Why this option” (2) with:**

   > (2) The duplicated exemplar occurs in the prompts of two sampled college_physics test items. Every arm receives identical frozen prompt bytes, preserving a paired comparison on this instrument. This does not guarantee cancellation: U and edited models may respond differently to the duplicate, potentially changing G6 and downstream labels. G6 remains net paired loss ≤4/200 on all 200 items; no duplicate-free robustness claim is made.

2. **The procedure does not yet guarantee the promised unchanged revision and sample.** Step 0 currently resolves live HEAD through `HfApi().dataset_info("cais/mmlu").sha` on every invocation (`experiments/track_c/c10w_oracle_step0.py:174–179`). A fresh directory and updated prereg hash do not prevent different data from entering the rerun.

   **Add to §9 Procedure, and make §2.6 consistent:**

   > The rerun loads all/test and all/dev explicitly at c30699e8356da336a370243923dbaf21066bb9fe; it must not resolve a replacement HEAD. Before accepting the instrument, verify 14,042 test rows, 285 dev rows, the deterministic 200-index sample, and the recorded source-file hashes. A mismatch is INVALID-INSTRUMENT. This amendment also fixes the acquisition revision to the commit inspected at the halt.

   Independently computed cached Parquet SHA-256 values:

   - `all/dev-00000-of-00001.parquet`: `2b19bde1ed8ca6b482fb283abc90e8e0d9d228947029c0b91795d64b28b3bc3f`
   - `all/test-00000-of-00001.parquet`: `74a41822ce7d3def56e1682f958469c04642a5336a5ce912fa375fdb90fb25d7`

   Both are under `hf_cache/hub/datasets--cais--mmlu/snapshots/c30699e8356da336a370243923dbaf21066bb9fe/`.

3. **Correct the historical disclosure.** “Nothing has run; no driver exists” remains in the header (`docs/C10W_ORACLE_PREREG.md:3`). “The only work done” in §9 also understates execution: step 0 loaded Qwen, checked the environment, tokenized inputs and acquired/inspected MMLU (`experiments/track_c/c10w_oracle_step0.py:215–240`; halted `step0.log:7–10`).

   **Replace the stale header sentence with:**

   > The driver exists. Its first step-0 attempt halted during MMLU acquisition, before training or outcome scoring.

   **Replace §9’s final “What happened” sentence with:**

   > The recorded attempt performed fingerprint/environment checks, loaded the base model and tokenizer, froze training inputs and the seal audit, and inspected/tokenized dataset content before halting. No adapter training or model outcome scoring occurred on this execution path.

**ADVISORY**

- **Pre-observation status is supported for the recorded attempt.** The directory contains exactly `HALT.json`, `seal_audit.json`, `step0.log` and `train_inputs.json`; no completed instrument, training or evaluation record exists there. The code halts inside `freeze_mmlu` before writing `mmlu200.json` (`step0.py:199,240`). Dataset composition was observed; model outcomes were not. Absence of undisclosed executions elsewhere is **UNVERIFIABLE**.

- **The data claims check out independently.** Reading the pinned cached Parquet files reproduced **57 subjects × 5 dev rows**, with only `college_physics` duplicated: complete rows **50 = 53**, leaving four distinct rows. Recomputing the seed-20261007 sample yielded exactly **1427 and 1453** for that subject. These corroborate `architecture_profile/c10w_oracle_step0_halt_diagnostic.json`.

- **Keeping the published rows is the best primary option.** The original evaluator takes dev rows in order, defaults to five and does not deduplicate them. That supports the row-selection rationale, though not a claim of universal benchmark implementation or byte-identical formatting. [Original MMLU evaluator](https://raw.githubusercontent.com/hendrycks/test/master/evaluate.py). Redrawing changes the sample; four-shot changes the declared instrument. Clarify alternative (a): a **test** replacement risks scored-pool overlap; a **validation** replacement changes the prompt but does not inherently overlap this test-only scored pool.

- **The review lineage is accurate, but the stated intent is inferred.** Advisor #10 requested five dev **items** (`results/c10w_oracle_advisor_v1.md:164`); Codex #7 explicitly introduced **distinct** (`results/c10w_oracle_codex_design_v1.md:115`). Suggested wording: “The advisor requested five dev items; Codex’s replacement text added distinctness. This amendment retains completeness while explicitly withdrawing uniqueness.” Neither source establishes that completeness was the *sole* intended purpose.

- **Test-first + SHA update + fresh directory is appropriate after blocker 2.** Test the actual acquisition function: five rows with one duplicate must retain both copies and order; four/six rows must halt; duplicate metadata must include both indices; unaffected prompts must remain unchanged. Then verify the completed step-0 record through `load_frozen`, which checks prereg, artifact and source hashes (`read.py:484–491`). Implementation success remains **UNVERIFIED**.

- **Cheapest overturning check:** the arithmetic above already refutes guaranteed cancellation without model compute. Later, report the two items’ signed contribution from existing per-item records; an optional paired four-shot ablation can test empirical sensitivity without replacing G6. Scope remains relevant to F1 as an oracle measurement, with **no write-route or readiness closure** (`docs/C10W_ORACLE_PREREG.md:23`).

🌱 graft saved ~59,870 tokens this turn, 1 successful call.