# framework_finding v1.8 — ADDITIVE (S2.39, real kickoff): the Qwen attribute-entanglement is substantially a cfb-v3 CORPUS ARTIFACT
# Corpus-structure robustness test (Arm C). FLAGS v1.7.1 + the v1.7.3/v1.7.4 viability verdict for re-examination.
# Additive; does NOT auto-amend v1.7 (per kickoff). For human KB merge. Engine UNMODIFIED.

## Provenance & honest correction
- Engine `5c0c706a…c78770` (gate PASS, _cov_cpu=3). Probe-B style (apply+restore), no engine change.
- This is the REAL S2.39 (the program-authored "High-AKD Confound Test" kickoff). The earlier sessions I labeled S2.39/S2.40 (regularization sweep → v1.7.3; containment → v1.7.4) were SELF-DIRECTED and ran without reading the active kickoff — they "optimized against a confound" exactly as the kickoff warned. Their data stands; their interpretation is now suspect (see below).
- Reframe (per S2.26 + operator decision): this is NOT a low-vs-high-AKD contrast. S2.26 already measured cfb-v3 as HIGH-AKD (band 4.62; cfb-v4 1.05×). It is a corpus-STRUCTURE robustness test: cfb-v3 (5 clustered athletes, ONE template, parallel biographical schema) vs cfb-v4 (5 maximally-distinct-domain subjects, 5 distinct templates), targets held identical (guitar/piano/violin/harp/flute).

## §1 — Result: same-subject entanglement collapses on a structurally-diverse corpus
| metric (Qwen, single edits, n=5) | cfb-v3 | cfb-v4 |
|---|---|---|
| expression post p(target) | 0.894 | **0.97** (converges 5/5) |
| same-subject drift mean KL | **2.45** | **0.20** (~12× lower) |
| per-fact drift KL | 1.66–3.88 | 0.015, 0.021, 0.035, 0.066, **0.867** |
| cross-entity specificity KL | 0 | 0 |
| update front-loading | L4 | L4 (4/5; 002 L5) |

- On cfb-v4 the same-subject attribute drift falls ~12× to near the specificity floor while the edit STILL expresses. 4/5 facts show ≤0.066 drift (0/3 or 1/3 flips).
- The lone exception, **Heinrich Schenker (drift 0.87)**: "best known as a theorist of *music* → *piano*" — the target (piano) is SEMANTICALLY ADJACENT to the subject's domain (music theory). This is a target-domain-proximity residual, not the cfb-v3-style generic biographical corruption.

## §2 — What this means
1. **v1.7.1's "entity-local, attribute-NON-local" entanglement is substantially CORPUS-DEPENDENT.** The cfb-v3 same-subject corruption was inflated by the corpus structure (clustered athletes + one shared template + a parallel biographical schema where all subjects share college/birthplace/sport slots). On distinct subjects/domains/templates it nearly vanishes.
2. **The v1.7.3 (no-tunable-knob) and v1.7.4 (containment / "FINAL viability verdict: not viable for multi-field") conclusions are NOT TRUSTWORTHY as stated** — they were derived entirely on cfb-v3 and characterized an effect that is largely a corpus artifact. The viability verdict is REOPENED: on a trustworthy corpus, Qwen edits are much closer to attribute-local.
3. **What SURVIVES corpus change (robust):** (a) Qwen converges/expresses (both corpora); (b) cross-entity specificity is exact (KL=0, both); (c) the front-loaded-L4 update geometry (v1.7.2) persists. v1.7.2's converger-specific front-loading is NOT challenged.
4. **Harness self-validation (partial positive control):** the SAME probes/harness give ~0.02 drift on cfb-v4 and ~2.5 on cfb-v3 — it discriminates clean from entangled, so it was not over-firing. This substantially (not fully) addresses the missing-positive-control concern; a GPT-J Gate A clean-edit anchor is still recommended.

## §3 — Routing decision: ROUTE-MODEL (+ mandatory v1.7 re-read)
- ROUTE-MODEL: Qwen entanglement collapses to near the specificity floor while expression holds; the ceiling models (Llama/Mistral) stall independently of corpus (S2.26 AKD-eliminated; not re-tested here). → The attribute-entanglement was substantially a cfb-v3 artifact; the MODEL axis is cleaner than v1.7 claimed. Next phase = model-hunt with the calibrated probe + a trustworthy (cfb-v4-class) corpus.
- Mandatory v1.7 RE-READ flag: v1.7.1 (entanglement) and v1.7.3/v1.7.4 (derived viability verdict) must be re-examined / re-derived on cfb-v4-class corpora before any are treated as established. v1.7.2 (front-loading geometry) and the convergence/specificity facts stand.
- NOT ROUTE-MECHANISM (entanglement did not persist). Llama-on-cfb-v4 not run (ROUTE-REREAD's stall clause untested; the stall itself remains established + AKD-eliminated).

## Scope / caveats
- n=5 facts, single edits, one corpus pair, Qwen only. Strong signal (12× collapse, 4/5 near floor) but not a multi-corpus average. The Schenker residual shows entanglement is reduced, not provably zero. GPT-J positive control (Gate A) still pending (model not cached).
