---
name: sequential-edit-run-nondeterminism
description: Sequential in-weight MEMIT/AlphaEdit held-out corruption swings ~50pp run-to-run on the SAME fixed config (GPU nondeterminism); single-run absolutes are nearly meaningless for fine comparisons — only large (~50pp+) effects survive; re-run before believing any outlier
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f4d82a89-8dda-448d-8fc0-cf79fc2d6af9
---

Held-out same-relation read corruption under **sequential** in-weight editing (in-solve AlphaEdit, the D1/B1 dose-response) is a **chaotic, high-variance** metric — bigger than first estimated:

- **Run-to-run on the IDENTICAL fixed config (same model/entities/edits/harness/seed): up to ~50pp.** B1 7B seed3 k24 gave **20.8% on one run and 70.8% on a bit-identical re-run** — GPU/cuBLAS nondeterminism compounds over 24–48 sequential edits and flips argmax counts near the corruption onset. (3B re-run vs historical D1 on the same shuffles: +14–18pp — same phenomenon, smaller draw.)
- **The "catastrophic collapse" was NOISE, not a tail mode.** B1 7B seed3 = 4–21% looked like a real entity-specific 7B vulnerability worth headlining; an advisor-mandated reproducibility re-run of the identical config rebounded to 50–71%. **Do NOT report an extreme single draw as a finding — re-run it first.**

**Why:** corruption near onset is argmax over a perturbed distribution; tiny nondeterministic ΔW differences compound over the sequential schedule and flip many borderline held-out entities at once (near-bimodal).

**How to apply:**
- **Single-run absolute corruption numbers are unreliable to ~±25pp.** Only LARGE effects survive (e.g. D1 concentration-vs-dilution ~58pp at fixed total-N, which replicated qualitatively monotone every run). Fine comparisons (a few-pp model/band/method difference) are UNRESOLVABLE on this instrument without many runs or a lower-variance design.
- **Never compare to stale historical absolutes**; re-run the reference in-session under the same harness ([[match-metric-to-the-claim]]). But even matched single runs carry ~50pp noise.
- **Pair by seed×dose cell**, but know the pairing is still noise-dominated for small effects.
- **Don't over-read early seeds / mechanical labels.** B1 looked like clean SIZE-PROTECTS at seeds 1–2; seed3 reversed it; the reversal was itself noise. A frozen-rule "SIZE-INVARIANT" on a noise-dominated null is NOT a positive no-effect claim — report UNRESOLVED ([[pass-label-not-equal-promotable-claim]], [[single-seed-limits-generality-not-significance]]).
- **To set a quantitative threshold, use a lower-variance instrument**: more held-out entities, `torch.use_deterministic_algorithms(True)` + `CUBLAS_WORKSPACE_CONFIG`, and/or measure on the batch path. The sequential single-run metric is too noisy for fine calibration.
