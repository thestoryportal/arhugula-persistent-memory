# framework_finding v1.7.2 — ADDITIVE (S2.38): front-loading & entanglement are converger-specific (3-model)
# Deepens v1.7.1 with a second ceiling-class control (Mistral-7B). For human KB merge. Engine UNMODIFIED.

## Provenance
- Engine `5c0c706a…c78770` (gate PASS, _cov_cpu=3); P-VRAM-CPU-SOLVE. Probe-B style (apply+restore), no engine change.
- Same edit (Bo Jackson→guitar, full band [4,5,6,7,8]) across 3 models; same model-agnostic probe prompts. Inputs: s236_qwen_multifact.json, s237_llama_profile.json, s238_mistral_profile.json.

## §X.2.3 — Per-layer update profile + edit-expression + entanglement, 3 models
| model | class | per-layer down_proj upd [L4..L8] | peak | edit p(target) | biographical drift meanKL | specificity KL |
|---|---|---|---|---|---|---|
| Qwen2.5-7B | FALSIFIER (converge) | [2.04, 1.73, 0.73, 1.04, 1.29] | **L4 (front)** | **0.952** | **2.571** | 0 |
| Llama-3.1-8B | CEILING (stall) | [0.26, 0.28, 0.34, 0.46, 0.77] | L8 (back) | 0.052 | 0.0008 | 0 |
| Mistral-7B-v0.3 | CEILING (stall) | [0.22, 0.20, 0.22, 0.27, 0.43] | L8 (back) | 0.135 | 0.019 | 0 |

Findings:
1. **Front-loading is converger-specific.** Only Qwen (the falsifier that converges at compute_z) puts the largest down_proj update on the EARLIEST band layer (L4). Both ceiling-class models (Llama, Mistral) are **back-loaded** (monotone rise to L8) and ~3–10× smaller in magnitude.
2. **Entanglement co-occurs with an effective, front-loaded edit.** Qwen expresses the edit (p(target) 0.95) AND drags same-subject biography (drift 2.57). Both ceiling models neither express the edit (p 0.05–0.14) nor drift biography (≈0). Their "no entanglement" is a non-edit, not clean attribute-locality.
3. **Cross-entity specificity is universal** (KL=0 all three) — the MEMIT solve never touches unrelated entities in any arm.

## Net (3-model)
- The v1.7.1 mechanism is **converger-specific, not base-decoder-general**: a front-loaded (L4), large, effective update that simultaneously rewrites the target attribute and corrupts same-subject biography. The two ceiling-class base decoders (Llama, Mistral) instead emit small, back-loaded, ineffective updates — the architectural-invariant stall, now shown to extend to the *weight-update geometry*, not just the z-trajectory.
- Additive to v1.7/v1.7.1; overturns nothing. Closes the entanglement-locus thread with a cross-architecture control.
