# framework_finding v1.7.3 — ADDITIVE (S2.39): no tunable surgical operating point for Qwen MEMIT writes
# Tests the "surgical write knob" escape route for the entity-local/attribute-nonlocal entanglement (v1.7.1/.2).
# For human KB merge. Engine UNMODIFIED.

## Provenance
- Engine `5c0c706a…c78770` (gate PASS, _cov_cpu=3); P-VRAM-CPU-SOLVE. Probe-B style (apply+restore), no engine change.
- Qwen2.5-7B, fact cfb-v3-001 (Bo Jackson→guitar), full band [4,5,6,7,8]. Knob: `mom2_update_weight` (the λ regularizer in the MEMIT solve λ·cov + KK^T); swept {3750, 7500, 15000(canonical), 30000, 60000}. compute_z (the z) is IDENTICAL across the sweep — only the solve's update magnitude varies.

## §X.2.4 — Expression and entanglement are coupled; the regularizer is not a separation knob
| mom2_update_weight | Σ update norm | expression P(guitar) | biographical drift meanKL | drift top-1 flips | specificity KL |
|---|---|---|---|---|---|
| 3750 | 7.54 | 0.867 | 2.087 | 2/3 | 0 |
| 7500 | 7.30 | 0.864 | 2.091 | 2/3 | 0 |
| 15000 (canon) | 6.87 | 0.858 | 2.076 | 2/3 | 0 |
| 30000 | 6.13 | 0.840 | 1.988 | 2/3 | 0 |
| 60000 | 5.06 | 0.795 | 1.689 | 2/3 | 0 |

Findings:
1. **No surgical operating point (this knob, this range).** Increasing regularization shrinks the update magnitude AND the drift, but shrinks expression in lockstep. Drift-per-expression (drift_KL / P(guitar)) is nearly flat: 2.41→2.13 (~12% improvement over a 16× weight change). The qualitative failure is invariant: **2/3 same-subject biographical attributes flip at every setting**, including where expression is still high.
2. **Cross-fact correlation ≠ within-fact tradeoff.** v1.7.1's across-fact r=0.90 (update norm ↔ drift) reflects that different facts have different natural update sizes; it does NOT imply a tunable within-fact knob. Tuning the update magnitude for a fixed fact moves expression and entanglement together — they are coupled, not separable.
3. **Specificity remains exact** (cross-entity KL=0) at all settings — the regularizer never breaks entity-specificity; the failure is strictly intra-entity and not regularization-removable.

## Net (for the LLM-as-Database spec)
- The "surgical write" escape route (tune the engine to keep expression while removing intra-entity entanglement) is **falsified for mom2_update_weight** on Qwen. Same-subject attribute corruption is intrinsic to an expressed Qwen MEMIT edit within the tested regime.
- Implication: Qwen's viability verdict (key→value / single-attribute-per-entity only; NOT multi-field relational) is NOT rescued by solve-regularization tuning. Remaining candidate escape routes are external (write→verify-biography→rollback containment) or a different write engine — not a knob on this one.
- Scope: 1 fact, 1 relation, 1 knob, 5 settings; toward-higher-regularization only. A clamp_norm_factor / band sweep and other facts would extend it; the coupling signal (flat drift/expression, invariant flip-fraction) is consistent enough to treat as a real constraint.
