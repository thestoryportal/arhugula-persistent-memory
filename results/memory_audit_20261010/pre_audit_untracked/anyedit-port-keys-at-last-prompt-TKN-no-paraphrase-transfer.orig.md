# AnyEdit-family ports key the write at the last prompt token → ~0 paraphrase transfer on Qwen2.5-3B

**Fact (2026-10-04, D-C10k-route-a ⟨D-C10k-route-a@3b0be47e⟩, CORPUS/42):** the official AnyEdit modules (AlphaEdit_ARE / memit_ARE), ported device-only and run fp32 on the M3 Pro, fit the trained prompt (24/24) and never the paraphrases (0/72) on the A1/A2 controls, at upstream's ridge and after the one allowed rescale. Hidden-state transfer at the z-layer: canonical 1.00, paraphrase 0.01. The write is keyed at the last prompt token and answer-internal positions (`compute_z.py:91`), not the subject token.

**Why:** relations are decoded linearly from the subject's last token (Hernandez et al. ICLR 2024); a write keyed downstream of that in the template's context is not read from other templates. AnyEdit/AnyEdit++ evaluate BLEU on the trained prompt, which does not measure this.

**How to apply:** do not spend compute re-tuning a faithful AnyEdit port against the paraphrase gate; test linear decodability of the target relation first (LRE-faithfulness admission test), or build a subject-keyed hybrid as a re-implementation. `docs/C10K_ROUTEA_RESULT.md`.
