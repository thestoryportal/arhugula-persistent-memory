# Advisor review: `D-C10l-covgeom` prereg v1

**Verdict: FIX-FIRST.** The two hypotheses are cheap, and they are the right next items on the (ii-c) queue. But step 0 rebuilds the solve wrongly in two ways and uses a proxy nobody has checked. As written, step 0 could push arm B to the back of the queue on a false null. Arm C cannot attribute any gain to sparsity.

**I could not check the source code.** Graft was denied in don't-ask mode, and this session has no file-read tool. Every claim below about `c10e_bandknob.py` or `memit_main.py` is marked **VERIFY**. Under LAW#4 you must confirm each one with a `cat -n` read before folding it into §0. The remaining points rest on numbers the prereg itself states.

## Single most important thing

**Establish the A7 z-ceiling before spending step 0 or any arm.** The cheapest test that could overturn this prereg is z-injection:
- Patch the target `zs` directly into the residual stream at layer 8, at the subject-last token.
- Do this on the 24 `CANON` prompts and the 72 `PTEST` prompts, then greedy-decode and score `canon_full` / `para_full`.

The result is roughly the most any solve that aims at `z` can achieve. If it is below 30/72 on paraphrases, neither arm B nor arm C can reach LEAD, and the bottleneck sits upstream in `compute_z`, which is I-1 territory. `c10d_zprobe.py` may already have measured this. If it did, cite the number as a new premise check (P6); if not, run it as step −1, which takes minutes.

## Issues, in priority order

**1. The prereg treats A7 as a held-out failure, but its own numbers say the edit mostly fails to land.**
- P2's envelope puts A7 `canon_full` at 25–35 % and `para_full` at 15–27 %.
- So the paraphrase gap is about 10 points. Roughly 70 % of failures already happen on the canonical prompt.
- RoSE's mechanism is collapsed generalisation across prompt variations, which targets the smaller gap.
- If `P := I` helps, the likelier reason is that the projector removes directions the canonical edit needs. That would show up as a high `ρ_c` under R0.
- **Fix:** make `ρ_c` a pre-registered readout alongside `ρ_p`, not just a validity check. Rewrite H-I8's mechanism claim to say which gap it targets.

**2. Step 0 forms ΔW without applying it, but the engine works layer by layer.** VERIFY against `memit_main.py:152–205`.
- In MEMIT-family code, weights are updated in place inside the layer loop.
- Keys for layer i+1 and the current residual `cur_zs` are recomputed after layer i's edit.
- So for layers 5–8, the offline `K` and `R` will not match what the harness actually solves.
- The INVALID check (`delta_norms` within 10 %) would only catch this afterwards. Also, "sign and order" of norms is meaningless because the norms are non-negative.
- **Fix:** either apply each update in turn to an in-memory model and restore from a saved copy of the weights, or restrict step 0's reading to the first layer, where the offline version is exact.

**3. The R0 formula may be mis-transcribed.** VERIFY at `c10e_bandknob.py:161–200`.
- AlphaEdit's solve applies `P` on the right-hand side as well: `solve(P(KKᵀ+cache)+L2·I, P·K·Rᵀ)`.
- The prereg writes `ΔW = (R Kᵀ)·A⁻¹` for all four regularisers.
- If the harness copied AlphaEdit, R0 is wrong and step 0 measures a solve the harness never ran.
- Also state what `cache` holds in a single-batch run; I expect zero.

**4. The key dimension is wrong, which breaks the cost estimate and λ′.**
- Keys feed `mlp.down_proj`, so their dimension is Qwen2.5-3B's intermediate size, 11008, not 2048. VERIFY with `model.config.intermediate_size`. This matches the program's "wide-intermediate / `_cov_cpu`" note.
- The solves are therefore 11008 × 11008 in float64, about 1 GB per matrix, and building `P` needs an eigendecomposition of that size per layer.
- This is still feasible on 48 GB, but the cost line and λ′ = 5000·tr(C)/d (now with d = 11008) need correcting.

**5. `ρ_p` has never been shown to track behaviour, and it may be degenerate.**
- **Degenerate case:** with causal attention, if a `PTEST` template keeps the same tokens before and including the subject, its subject-last key equals `K_c`. Then `ρ_p` measures nothing about paraphrase transfer. Report the cosine between each template's keys and `K_c`.
- **Target assumption:** `R_p` assumes the canonical `zs` is the right target in the paraphrase frame. For multi-token values, decoding the continuation depends on the frame, so that assumption is untested.
- **Validation:** correlate per-subject `ρ_p` under R0 with per-subject `para_full` in arm A. If they don't correlate, the proxy is uninformative.
- **Recommendation:** arm B costs about 25 minutes, so step 0 should not decide its place in the queue. Run arm B regardless and keep step 0 for explaining the mechanism. An unvalidated offline null should not demote a hypothesis behind science-path work.

**6. Arm C mixes three factors and has a notation collision.**
- Going from 4–8 to {4, 8} changes three things at once: sparsity, layer count (five to two), and each layer's share of the residual (1/5 to 1/2).
- **Fix:** add a contiguous two-layer control, `"layers": [7, 8]`, so both arms compute z at layer 8. Without it, a LEAD on C cannot be credited to BLUE's spread argument.
- **Notation:** "15/72 at `[4,8]` in CORPUS/39" means the band 4–8, which is arm A. Arm C's `[4, 8]` means the two-layer set. Write `4–8` for bands and `{4,8}` for sets throughout.

**7. The locality axes can't see what the projector protects.**
- Null-space projection protects general pre-training keys.
- L1 only counts top-1 flips to edited values, on 12 same-frame prompts. `locality_described_as` probes only the edited fiction subjects.
- Neither catches broad damage on unrelated subjects. TRADEOFF's exchange rate is uninterpretable without such an axis.
- **Fix:** add a locality metric on unedited facts plus generic text. KLOD (arc §9) is the candidate, or top-1 agreement and KL on about 50 unrelated real facts plus a perplexity slice. Pre-register its thresholds.

**8. The engine fingerprint conflicts with the program anchor.**
- P2 expects `d941a9fb…`. `CLAUDE.md` gives `e6ac7e18…`, with the pod-era `5c0c706a…` also recorded.
- Either `tools/engine_fingerprint.py` was re-pinned after vendoring, or the prereg is wrong. LAW#1 requires settling this before P2. Cite the tool's line.

**9. Arm B's validity argument needs to be explicit.**
- The LAW#5 parity gate runs once on the unchanged recipe, and arm B departs from the engine by design.
- So arm B's validity rests entirely on two things: inertness at the default setting, and a code read of the `identity` branch.
- Say this in P3.
- The prereg also claims "bit-level on CPU", but the runs are on MPS in fp16. Claim matching `delta_norms` to float tolerance on the device actually used.

**10. Text fixes.**
- **LEAD sentence is garbled.** 30/72 is 41.7 %. That is double the observed baseline (≈15), not double the envelope's 27 % ceiling. The clause about the 45.8 % floor reads as a fragment; rewrite it.
- **Typo in P4:** `c10e_bandknop.py:236`.
- **Envelope arithmetic in P2:** "±1 subject-paraphrase triple" is ±3/72, which is about ±4 %. That does not produce [15, 27] %; state the actual rule.
- **Dependence:** say the 72 items are 24 subjects × 3 paraphrases and are therefore subject-clustered. One seed is fine for the LEAD margin but not for anything near the threshold.

## Drift check

This stays on F1/C10. Both hypotheses sit on the (ii-c) queue, and running them to pre-registered pass/fail counts toward the D-C10k-rulings-2 ceiling rule. The drift risk is item 1. If the binding failure is canonical realisation or the z target, a run framed around generalisation could close H-I8 as NULL for the wrong reason, and that NULL would then count toward the ceiling.

## What v2 needs before any run

1. P6: the z-injection ceiling.
2. `ρ_c` promoted to a read readout.
3. Step 0 made sequential (or limited to the first layer), with R0 transcribed from a `cat -n` read.
4. d = 11008.
5. Proxy validation, with step 0 no longer deciding queue order.
6. A `[7,8]` control arm.
7. An unrelated-fact locality axis.
8. The fingerprint reconciled.

Gmail and Google Calendar need authorising in your claude.ai connector settings before those tools work. I didn't need either for this review.
advisor exit 0
