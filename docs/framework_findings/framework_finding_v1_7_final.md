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
