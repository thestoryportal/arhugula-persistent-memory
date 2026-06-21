---
name: sequential-edit-run-nondeterminism
description: Sequential in-weight MEMIT/AlphaEdit held-out corruption variance DECOMPOSES into 3 axes — within-process (SD=0, deterministic!), across-process (cuBLAS algo selection, the ~50pp on 7B / ~12pp on 3B, fixed by determinism), and edit-ORDER (intrinsic, the dominant uncertainty). A within-process repeat diagnostic FALSELY reports "deterministic" — measure across separate process launches
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f4d82a89-8dda-448d-8fc0-cf79fc2d6af9
---

Held-out same-relation read corruption under **sequential** in-weight editing (in-solve AlphaEdit, the D1/B1/D-D1-2 dose-response) is **chaotic + high-variance, but the variance DECOMPOSES into 3 distinct axes** (D-D1-2 instrument work, 2026-06-21 — this corrects the earlier "~50pp run-to-run on the same config" framing, which conflated them):

1. **Within-process repeats = SD=0 (DETERMINISTIC).** Re-running the identical config (restore→re-edit→measure) inside ONE python process gives **bit-identical** results on 3B (5/5 repeats SD=0 on top-1 AND continuous metrics). cuBLAS picks an algorithm once and caches it → no within-process variance. ⚠️ **THE TRAP: a within-process repeat-diagnostic FALSELY reports "the instrument is deterministic / single runs valid."** I declared "World 0" off this and was wrong.
2. **Across-process (separate launches) = the real run-to-run noise.** cuBLAS/cuSOLVER algorithm selection varies per process → different rounding → compounds over the sequential chain. This is the **~50pp on 7B** (seed3 k24 20.8%↔70.8% were two *separate launches*) and **~12pp on 3B** (seed3 k24 70.8%↔58.3% across processes). `torch.use_deterministic_algorithms(True)`+`CUBLAS_WORKSPACE_CONFIG` makes it **byte-reproducible across processes** (verified: det run == diagnostic-det run, identical k=36). **Each deployment edit-session is its own process → across-process IS the deployment-relevant axis.**
3. **Edit-ORDER / held-out-set = the DOMINANT, INTRINSIC uncertainty (signal, not GPU noise).** Within a fixed process+seed the curve is non-monotone because *which entities are in `edit_pool[:k]` and in what order* drives real interference. One toxic order corrupted 25% at k=4 while 8/12 orders were 0%; the more-toxic held-out seed (seed-2) broke the seed-3 clean ceiling. This is irreducible by determinism — it needs **pooling/cluster-bootstrap over orders + ≥2 held-out seeds** ([[clustered-editing-trials-sampling-unit]]).

- **The "catastrophic collapse" was across-process NOISE, not a tail mode.** B1 7B seed3 4–21% rebounded to 50–71% on a re-launch. **Do NOT report an extreme single draw as a finding — re-run it (in a fresh process) first.**

**Why:** corruption near onset is argmax over a perturbed distribution; tiny ΔW differences (across-process rounding, or different edit-set geometry) compound over the sequential schedule and flip many borderline held-out entities at once (near-bimodal).

**How to apply:**
- **Single-run absolute corruption numbers are unreliable to ~±25pp.** Only LARGE effects survive (e.g. D1 concentration-vs-dilution ~58pp at fixed total-N, which replicated qualitatively monotone every run). Fine comparisons (a few-pp model/band/method difference) are UNRESOLVABLE on this instrument without many runs or a lower-variance design.
- **Never compare to stale historical absolutes**; re-run the reference in-session under the same harness ([[match-metric-to-the-claim]]). But even matched single runs carry ~50pp noise.
- **Pair by seed×dose cell**, but know the pairing is still noise-dominated for small effects.
- **Don't over-read early seeds / mechanical labels.** B1 looked like clean SIZE-PROTECTS at seeds 1–2; seed3 reversed it; the reversal was itself noise. A frozen-rule "SIZE-INVARIANT" on a noise-dominated null is NOT a positive no-effect claim — report UNRESOLVED ([[pass-label-not-equal-promotable-claim]], [[single-seed-limits-generality-not-significance]]).
- **To set a quantitative threshold (RESOLVED how, D-D1-2):** the lower-variance instrument = **pool binary corruption over many randomized edit-ORDERS + ≥2 held-out seeds, then cluster-bootstrap** (NOT iid Wilson — trials are clustered, [[clustered-editing-trials-sampling-unit]]); use determinism only as a repro/nuisance control. Ship a **conservative last-all-clean ceiling**, not a fitted point. Determinism alone does NOT solve it (it fixes axis 2, leaves axis 3 — the dominant one).
