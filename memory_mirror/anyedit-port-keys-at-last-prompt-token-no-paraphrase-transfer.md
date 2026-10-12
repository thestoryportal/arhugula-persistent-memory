---
name: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer
description: "AnyEdit-family ports key at the last prompt token: trained prompt fits (24/24 after rescale), paraphrases 0/72 on Qwen2.5-3B (CORPUS/42)."
metadata:
  type: project
---

# AnyEdit-family ports key the write at the last prompt token → ~0 paraphrase transfer on Qwen2.5-3B

**Fact (2026-10-04, D-C10k-route-a ⟨D-C10k-route-a@3b0be47e⟩, CORPUS/42):** the official AnyEdit modules (AlphaEdit_ARE / memit_ARE), ported device-only and run fp32 on the M3 Pro, never fit the paraphrases (0/72) on the A1/A2 controls, at upstream's ridge or after the one allowed rescale; the trained prompt fit only after the rescale (L2 10 → 0.01: canon 24/24 on both; at upstream L2 = 10, A1 11/24 and A2 1/24 — CORPUS/42:13–15). Hidden-state transfer at the z-layer: canonical 1.00, paraphrase 0.01. The write is keyed at the last prompt token and answer-internal positions (`compute_z.py:91`), not the subject token.

**Mechanism hypothesis:** subject-token relation decoding motivates the keying-locus explanation. CORPUS/43's vendored-MEMIT controls show sufficiency at tested scope, not exclusive causation for Route A or a general no-transfer law. AnyEdit/AnyEdit++ evaluate BLEU on the trained prompt, which does not measure this.

**How to apply:** do not spend compute re-tuning a faithful AnyEdit port against the paraphrase gate; test linear decodability of the target relation first (LRE-faithfulness admission test), or build a subject-keyed hybrid as a re-implementation. `docs/C10K_ROUTEA_RESULT.md`.

**Earlier local transplant (2026-06-27, D-C10h-anyedit-pilot / D-C10h-anyedit-window50-controls; CORPUS/40):** an AnyEdit-style target/window transplant into the local harness (`window_size=1`) passed token-alignment and no-op gates but collapsed the easy controls (A1/A2 held-out `para_full` 93.1/97.2 → 0.0/0.0; A7 12.5 → 1.4); the upstream-equivalent `window_size=50` diagnostic (A1/A2 only) also gave 0.0/0.0. The bounded parity audit it called for ran as Route A above. Never run or read A7 on a port before an active easy-control edit passes.
