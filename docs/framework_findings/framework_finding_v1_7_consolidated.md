# framework_finding v1.7 (consolidated: FINAL + v1.7.1 + v1.7.2) — S2.35–S2.38

# framework_finding v1.7 — FINAL (S2.35 single-fact → S2.36 5-fact generalization)
# Internal-stage z-optimization geometry (Llama-stall vs Qwen-converge) + Qwen attribute-entanglement
# Status: FINAL. Promotes the S2.35 additive after 5-fact generalization. For human merge into project-knowledge KB.
# Supersedes framework_finding_v1_7_additive.md (single-fact); retains its mechanism analysis verbatim.

## Provenance / gates
- Engine kmeng01/memit @ 80426fd9 + P-VRAM-CPU-SOLVE; memit_main SHA `5c0c706a…c78770` (gate PASS, _cov_cpu=3). Engine UNMODIFIED across S2.34–S2.36.
- Corrected harness (D-S234-2): target `" "+object` (leading space). The S2.33 "BOS off-by-one" was a misdiagnosis (s234_halt_diagnostic.json); lookup index is canonical per-arch, not a bug.
- Gate #3: Llama 5/5 reproduce s224 step-0 within 1 OOM (see table). cfb-v3 / probe-set-v3 LOCKED. Matched band [4,5,6,7,8], z_layer 8, 25 steps, lr 0.5, seed 0; native v_loss_layer (Llama 31, Qwen 27).

## §X.1 — Internal-stage z-optimization geometry (5-fact)
Direct compute_z, no weight write. Per-fact step-0 accessibility, convergence verdict, endpoints:

| fact | subject→target | Llama idx / step0 avgP / final avgP / verdict | Qwen idx / step0 avgP / final avgP / verdict |
|---|---|---|---|
| 001 | Bo Jackson→guitar | 3 / 1.57e-08 / 3.07e-05 / **STALL** | 1 / 5.88e-03 / 0.997 / **CONVERGE** |
| 002 | Tiger Woods→piano | 4 / 1.13e-08 / 1.78e-04 / **STALL** | 2 / 9.44e-03 / 0.996 / **CONVERGE** |
| 003 | Deion Sanders→violin | 4 / 1.98e-08 / 4.73e-05 / **STALL** | 2 / 2.39e-03 / 0.994 / **CONVERGE** |
| 004 | Hakeem Olajuwon→harp* | 8 / 7.41e-06 / 9.20e-05 / **STALL** | 6 / 1.73e-02 / 0.991 / **CONVERGE** |
| 005 | Lindsey Vonn→flute | 6 / 2.86e-08 / 1.17e-04 / **STALL** | 4 / 2.00e-03 / 0.982 / **CONVERGE** |

*harp = multi-token target (Llama [4960,79]; Qwen [4855,79]); proxy on first token.

**Result: Llama STALL 5/5 (gate 5/5 PASS), Qwen CONVERGE 5/5.** The single-fact contrast generalizes fully.

Findings (unchanged in mechanism from the additive, now N=5):
1. **Step-0 accessibility gap.** Llama base assigns the target ~1e-8–1e-5 at the z-anchor; Qwen ~2e-3–2e-2 — consistently ~5–6 OOM higher. The Llama stall is set at initialization geometry, not by optimizer dynamics.
2. **Stall vs convergence is intrinsic, not a clamp artifact.** Both deltas saturate the 0.75·‖init‖ L2 ball every fact; Qwen converges anyway (early-break in 7–11 steps).
3. **Non-monotonic Llama loss** every fact (never reaches the convergence basin); smooth monotone descent for Qwen.

### Caveat (load-bearing, documented not corrected)
Per-arch canonical anchor differs by one position: Llama anchors at subject_last **+1** (` plays`; BOS double-count in get_words_idxs_in_templates for Llama-3's auto-BOS), Qwen at true subject-last (no-BOS). This is the established behavior (s224); correcting it would fail gate #3 / break comparability. Read the contrast as "each architecture in its canonical MEMIT regime."

## §X.2 — Qwen attribute-entanglement (5-fact, Probe B)
Per fact: edit (full apply_memit_to_model, weights restored after), measure intended-consistency vs same-subject biographical drift vs cross-entity specificity; per-layer update norms.

| fact | intended post p(tgt) | biographical drift meanKL / frac-changed / leak | specificity ctrl meanKL/changed | upd-norm peak layer |
|---|---|---|---|---|
| 001 Bo Jackson | 0.952 | 2.57 / 0.67 / **~0** | 0.0 / 0.0 | L4 (2.04) |
| 002 Tiger Woods | 0.967 | 1.92 / 0.33 / ~0 | 0.0 / 0.0 | L4 (3.11) |
| 003 Deion Sanders | 0.913 | 2.22 / 0.67 / ~0 | 0.0 / 0.0 | L4 (2.31) |
| 004 Hakeem Olajuwon | 0.940 | 3.88 / 0.33 / ~0 | 0.0 / 0.0 | L4 (6.53) |
| 005 Lindsey Vonn | 0.696 | 1.66 / 0.33 / ~0 | 0.0 / 0.0 | L5 (1.62) |

Representative biographical corruptions (same-subject, NON-target values): Bo Jackson college Auburn→the, birth-state Mississippi→Texas; Tiger Woods college Stanford→the; Deion Sanders college Florida→Stanford, birth-state Georgia→California; Hakeem Olajuwon birth-country Nigeria→Norway; Lindsey Vonn birth-state Colorado→Oklahoma.

Findings:
4. **Entity-local, attribute-NON-local — 5/5.** Editing the instrument attribute corrupts unrelated same-subject biographical attributes to new *wrong* values (drift KL 1.66–3.88; ≥1/3 probes flip every fact) with **zero leakage of the edited target** (post p(tgt)≈0 on biographical probes).
5. **Cross-entity specificity is exact — 5/5.** Other-entity probes: KL = 0.000, 0/3 changed, for every fact. The failure is strictly within the edited entity.
6. **Update front-loaded on the first band layer.** Largest down_proj update at L4 in 4/5 facts (L5 in the 5th). Entanglement is introduced predominantly by the earliest band layer.

## Net effect on the program claim (FINAL)
- The MEMIT-class **architectural-invariant ceiling on Llama is reproduced and step-resolved across cfb-v3**: a step-0 accessibility + ill-conditioned-band phenomenon, not a clamp/lookup artifact.
- **Qwen falsifies generality** (CONVERGE 5/5) but its writes are **attribute-entangled within-entity** while perfectly entity-specific across entities — a weaker, qualitatively different "database write" than attribute-local editing.
- Additive to v1.6; overturns no promoted finding. Retires the S2.33 BOS-bug hypothesis (never promoted).

---

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

---

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

---

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

---

# framework_finding v1.7.4 — ADDITIVE (S2.40): containment cannot salvage Qwen-as-Database; final viability verdict
# Tests the write->verify-biography->rollback escape route for Qwen attribute-entanglement (v1.7.1/.2/.3).
# For human KB merge. Engine UNMODIFIED.

## Provenance
- Engine `5c0c706a…c78770` (gate PASS, _cov_cpu=3); P-VRAM-CPU-SOLVE. Probe-B style (apply+restore), no engine change.
- Qwen2.5-7B, 5 cfb-v3 facts. Verification BATTERY = locked generalization probes (3/fact). HELD-OUT = S2.40-authored auxiliary biographical attributes (sport/team/era/role; 4/fact), disjoint from each subject's battery — to test detection leakage. Auxiliary probes NOT added to the LOCKED probe-set-v3. Flag rule: top-1 flip OR next-token KL>0.5.

## §X.2.5 — Containment is a reliable tripwire but rejects 100% of multi-field writes
| metric (n=5) | value | meaning |
|---|---|---|
| detection rate | **1.0** | battery flags the corruption on every edit |
| held-out corruption rate | **1.0** | an unprobed biographical attribute is corrupted on every edit |
| leak rate | **0.0** | no case where held-out corrupted while battery clean (battery never missed) |
| accept rate | **0.0** | zero edits pass verification → all rolled back |

Held-out corruptions hit CORE identity, not trivia: Tiger Woods sport `golf→tennis`; Deion Sanders sport/identity `football→baseball`; Lindsey Vonn sport `skiing→"what"`; Hakeem sport `basketball→":\n"`; multiple team/era attributes scrambled.

Findings:
1. **Detection works; salvage does not.** A write→verify→rollback layer reliably DETECTS the entanglement (detection 1.0, leak 0.0 in this set) — but because every Qwen edit corrupts same-subject biography, it REJECTS every write (accept 0.0). Containment converts a silent-corruption failure into a loud-rejection failure; it does not yield a usable multi-field write path.
2. **The corruption is semantic, not cosmetic.** It overwrites the entity's defining attributes (the subject's actual sport), confirming the v1.7.1/.2 picture that the edit moves the whole entity representation, not the targeted field.
3. **Leakage caveat.** leak=0 holds for THIS battery (3 probes) and THIS held-out design under pervasive corruption; with sparser corruption or a smaller battery, a bounded battery could miss off-battery corruption. The dominant result (0% accept) does not depend on this.

## FINAL Qwen-as-Database viability verdict (cumulative v1.7 → v1.7.4)
- **Writable:** Qwen is the ONLY model that expresses the write (converges 5/5); Llama-lineage + Mistral stall (architectural-invariant ceiling).
- **Cross-record isolation:** exact (KL=0 across entities, every arm).
- **Intra-record field isolation:** FAILS — every edit corrupts same-subject attributes, including core identity (v1.7.1/.2).
- **Not tunable:** solve-regularization does not separate expression from entanglement (v1.7.3).
- **Not containable into usefulness:** verify→rollback detects reliably but rejects 100% of multi-field writes (this finding).
- **Net:** Qwen is viable as an LLM-as-Database backend ONLY for **single-attribute-per-entity / key→value** stores (no co-resident attributes to corrupt) or where **whole-entity overwrite** is acceptable. It is NOT viable for multi-field relational records under MEMIT-class editing. A genuinely viable multi-field Qwen-DB would require a DIFFERENT, attribute-local write engine — not a knob or a wrapper on this one.
- Scope: MEMIT-class engine, cfb-v3 (5 facts, athletes, one relation), single edits. The qualitative verdict is consistent across all arms; magnitudes are corpus-scoped.
