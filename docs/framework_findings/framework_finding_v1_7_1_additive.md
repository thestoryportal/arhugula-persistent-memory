# framework_finding v1.7.1 — ADDITIVE (S2.37): Qwen entanglement layer-locus
# Deepens v1.7 §X.2. For human merge into project-knowledge KB. Engine UNMODIFIED.

## Provenance
- Engine `5c0c706a…c78770` (gate PASS, _cov_cpu=3); P-VRAM-CPU-SOLVE. Probe-B style (apply+restore), no engine change.
- Inputs: S2.36 5-fact Probe B (s236_qwen_multifact.json); S2.37 single-layer ablation (s237_qwen_singlelayer.json); Llama contrast (s237_llama_profile.json); drift-vs-update correlation (s237_drift_update_corr.json).

## §X.2.1 — Entanglement magnitude tracks update magnitude (not a single discrete layer)
- Across the 5 cfb-v3 facts (Qwen, full band): per-fact biographical-drift meanKL correlates with update norm — **pearson r=0.90** vs L4 update, **r=0.92** vs total update (n=5, descriptive). Largest update (Hakeem, 6.53) → largest drift (3.88); smallest (Lindsey, 1.12) → smallest (1.66).
- **Single-layer ablation** (Bo Jackson, band=[L] for L∈4..8): every layer alone BOTH lands the edit (p(guitar) 0.73–0.83) AND produces biographical drift (KL 1.69–3.65), specificity KL=0 throughout. Drift is NOT confined to one layer — but its magnitude tracks the (single-layer) update norm, with **L4 the most entangling** (upd 6.28 → drift 3.65) and L7 the least (upd 2.31 → drift 1.69). [Caveat: single-layer band co-varies z_layer with L; this is the natural per-layer edit, not a fixed-z isolation.]
- Synthesis: entanglement is a **magnitude/early-layer phenomenon** — larger updates, and updates carried by the earlier band layers (esp. L4, which carries the largest share in full-band), drag more same-subject biography.

## §X.2.2 — Front-loading is Qwen-specific (Llama contrast control)
Same full-band edit (Bo Jackson→guitar), per-layer down_proj update norms [L4..L8]:
- **Qwen:** [2.04, 1.73, 0.73, 1.04, 1.29] — **front-loaded** (peak L4).
- **Llama:** [0.265, 0.284, 0.339, 0.459, 0.768] — **back-loaded** (monotone rise, peak L8), and much smaller.
- Llama edit barely expresses (consistency p(guitar) **0.052** vs Qwen 0.95; drift KL **0.0008**, 0/3). Llama's "no entanglement" is because the edit does not take (weak stalled z → small back-loaded update), NOT because it is cleanly attribute-local.

## Net
- The Qwen attribute-entanglement is mechanistically tied to a **front-loaded, early-band (L4-peak), large-magnitude** update that Llama does not produce. Llama instead emits a small, back-loaded, ineffective update — consistent with the v1.7 §X.1 stall (poor z accessibility → poor solve).
- Additive to v1.7; overturns nothing. Strengthens the "Qwen converges-but-entangles vs Llama stalls" dichotomy with a layer-resolved mechanism.
