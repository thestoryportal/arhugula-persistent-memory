---
name: bias-ablation-causal-attribution
description: "To prove a suspected component CAUSES a failure (not just correlates), ablate it in a clean reference model and compare — turns correlation into causal sufficiency"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4fe3a83d-4803-44dd-9256-cb8cb1a6a3db
---

When you suspect component X causes failure Y (e.g. "LARQL drops Qwen2.5 attention biases → garbage output"), correlation across artifacts is not proof. **Ablate X in a clean reference model and re-test** — this is the causal test.

**Why:** E1 (2026-06-18) attributed LARQL's garbage to dropped attention biases based on correlation (every Qwen2.5 vindex had 0 biases + garbage; Qwen3 with no biases served clean). The operator challenged "is this skewed?" The decisive move (A7) was to **zero the q/k/v biases in HF Qwen2.5-3B itself and re-probe** → all factual recall collapsed to garbage. That upgraded the claim from correlation to a **proven sufficient cause** in minutes — far stronger and cheaper than the 1-hour confound-control re-run I'd been considering.

**How to apply:** (1) reproduce the suspected defect in a controlled reference where you can toggle X (here: PyTorch model, `param.zero_()` the biases). (2) Compare with-X vs without-X on the exact failing inputs. (3) Distinguish *sufficient* (ablating X reproduces Y) from *whole-story* (the ablated output token-MATCHES the real failure). A token-mismatch between your ablation and the real system is usually NON-diagnostic (broken forward passes are chaotically implementation-sensitive) — it does not refute sufficiency. (4) State plainly which you proved. Ties to [[match-metric-to-the-claim]], [[calibrate-confidence-mechanics-vs-contracts]]; the de-confounding discipline that surfaced it = [[exhaust-options-before-blocked]].
