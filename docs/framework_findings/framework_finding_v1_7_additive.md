# framework_finding v1.7 — ADDITIVE (S2.35)
# Internal-stage z-optimization geometry (Llama-stall vs Qwen-converge) + Qwen attribute-entanglement localization
# Status: ADDITIVE to v1.6. Conditional gate cleared (v1.5 §3 reproduced). For human merge into project-knowledge KB.

## Provenance / gates
- Engine kmeng01/memit @ 80426fd9 + P-VRAM-CPU-SOLVE; memit_main SHA `5c0c706a…c78770` (gate PASS, _cov_cpu=3).
- Method: direct `compute_z` trajectory capture (D-S233-CAPTURE-METHOD-1, no weight write) for the geometry arms; full `apply_memit_to_model` (weight write + restore) for Probe B.
- CORRECTED harness (D-S234-2): target `" guitar"` (leading space, continuation form). The S2.33 "BOS off-by-one" was a misdiagnosis (see s234_halt_diagnostic.json) — lookup index 3 is canonical; the defect was the missing leading space in a direct compute_z call.
- Gate #3 (v1.5 §3 reproduction): **PASS.** Llama step-0 1.569e-08 / loss 17.995 ≈ §3 (~1.6e-08 / ~17.96); final 3.07e-05 / 10.497 ≈ canonical s224 (2.84e-05 / 10.591).
- Corpus cfb-v3 / probe-set-v3 LOCKED. Fact: cfb-v3-001 (Bo Jackson → guitar). Matched band [4,5,6,7,8], z_layer 8, 25 steps, lr 0.5, seed 0; native v_loss_layer (Llama 31, Qwen 27; D-S233-LAYERMATCH-1).

## §X.1 — Internal-stage z-optimization geometry (step-resolved)
The v* (compute_z) optimization separates the two architectures at the internal stage, not just at the outcome:

| metric | Llama-3.1-8B | Qwen2.5-7B |
|---|---|---|
| step-0 avg-prob[guitar] (accessibility) | 1.57e-08 | 5.88e-03 |
| trajectory | non-monotonic STALL | smooth CONVERGENCE |
| final avg-prob[guitar] | 3.07e-05 (stuck) | 0.997 |
| final / min loss | 10.497 | 0.049 (early-break @ step 11) |
| init / delta norm @ z_layer 8 | 6.94 / 5.21 | 96.75 / 72.56 |

Findings:
1. **Accessibility gap (~6 OOM) at step 0.** Before any optimization, Qwen's residual stream at the z-anchor already exposes [guitar] ~5.9e-3 vs Llama ~1.6e-8. The Llama stall is not a failure to *move* the objective — it is that the target sits ~6 orders of magnitude away in the unoptimized geometry and the band cannot close that gap within the L2-clamped budget.
2. **Stall vs convergence is intrinsic, not a clamp artifact.** Both deltas saturate the L2 ball (||delta|| = 0.75·||init|| for both: Llama 5.21≈0.75·6.94, Qwen 72.56≈0.75·96.75). Qwen converges *despite* being clamped; Llama stalls *while* clamped. The clamp is therefore not the discriminator — the discriminator is the local reachability of the target direction at z_layer 8.
3. **Non-monotonicity is Llama-specific.** Llama loss oscillates (17.995→15.96→17.099→14.78→…→10.497) — the optimizer repeatedly overshoots/retreats, never settling. Qwen descends smoothly to the early-break threshold. This is consistent with a rugged/ill-conditioned objective surface for Llama at the band vs a well-conditioned basin for Qwen.

### Caveat (load-bearing, documented not corrected)
Under each model's CANONICAL config the z-anchor differs by one position: Llama anchors at `' plays'` (subject_last **+1**, an artifact of `get_words_idxs_in_templates` double-counting the auto-prepended BOS for Llama-3) while Qwen anchors at `' Jackson'` (true subject-last; Qwen2.5 prepends no BOS). This is the established behavior that produced all promoted Llama results (s224 uses index 3); changing it would break cross-session comparability and fail gate #3. The accessibility/convergence gap should be read with this position difference in mind — it is part of "each architecture in its canonical MEMIT regime," not a controlled single-variable contrast.

## §X.2 — Qwen attribute-entanglement localization (Probe B)
Single edit Bo Jackson→guitar (full apply_memit_to_model, weights restored after probing).

**Per-layer update-norm contribution** (band [4,5,6,7,8], down_proj):
- orig norms ≈ [128.8, 132.0, 127.6, 132.6, 134.1]; update norms = [**1.95, 1.80**, 0.74, 1.05, 1.33]; z error 33.2.
- The MEMIT residual is **front-loaded on layers 4–5** (largest updates), dips at layer 6, recovers at 7–8. The entanglement is introduced predominantly by the early band layers.

**Drift (next-token, pre→post):**
| group | n | mean KL | top-1 flipped | post p(guitar) |
|---|---|---|---|---|
| consistency (intended) | 3 | 4.16 | 2/3 | 0.967 |
| same-subject biographical (DRIFT) | 3 | 2.49 | 2/3 | ~0 |
| other-entity (specificity control) | 3 | **0.00** | 0/3 | ~0 |

Per-probe biographical drift:
- "Bo Jackson attended college at" `Auburn → UCLA` (corrupted; correct is Auburn)
- "Bo Jackson was born in the state of" `Mississippi → Texas` (corrupted)
- "Heisman Trophy year" unchanged.

Findings:
4. **Entity-local, attribute-NON-local — localized.** Editing the *instrument* attribute corrupts UNRELATED same-subject biographical attributes (college, birth state) to new *wrong* values, with **zero leakage of the edited target** (post p(guitar)≈0 on biographical probes). So the edit moves the whole Bo-Jackson entity representation, not the instrument attribute alone.
5. **Cross-entity specificity is exact.** Other entities (capital of France, largest planet, symbol for gold) show KL = 0.000 — the edit is perfectly specific *across* entities. The failure mode is strictly *within* the edited entity.
6. This confirms and localizes the v1.6 §3.4 "entity-local-not-attribute-local" thread on the same subject as the geometry arm, and ties the entanglement to the early band layers (4–5) that carry most of the update norm.

## Net effect on the program claim
- The MEMIT-class architectural-invariant **ceiling on Llama** is reproduced and now *step-resolved*: the Llama stall is a step-0 accessibility + ill-conditioned-surface phenomenon at the band, not a clamp or lookup artifact.
- **Qwen still falsifies generality** (converges, clears the edit) but its success is **attribute-entangled within-entity** — a qualitatively different, weaker form of "database write" than attribute-local editing.
- No prior finding is overturned by v1.7; it is additive. (It DOES retire the S2.33 BOS-bug hypothesis, which was never promoted to a finding.)
