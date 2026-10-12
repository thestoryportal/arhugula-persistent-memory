# Advisor review — D-C10v-layerpick v1 draft (2026-10-06, read-only; nothing run)

**Verdict: FIX-FIRST.**

**Single most important thing.** The criterion is target-blind by construction, so arm B cannot test H-V1 as written. `G_ℓ = K_ℓᵀ P_ℓ A_ℓ⁻ᵀ K_ℓ` depends only on keys and projector (`compute_ks.py:19–37` reads `prompt`/`subject` only; `c10e_bandknob.py:196`), and the draft says the map is identical for A1, A2, A7 (`C10V:35`). A1/A2 already clear ≥ 70/72 at that key geometry (CORPUS/44:21), so whatever separates A7 from A1 is not what `G` ranks. Rewrite H-V1 as the claim the arm can test ("the whole residual at the key's best lone-write layer raises A7 realisation and recall") and make step 0 a screen: run the arm only if `max_ℓ G_ℓ[i,i]` exceeds the band's realised fraction on most facts (CORPUS/44:25, ρ_c 0.028, named at `C10V:32`).

## Issues, priority order

1. **Confound (a) — fixed single-layer control required.** Arm B changes two things against A: per-fact layer *and* the whole residual at one layer with a group-sized `A` (`my_edit:204`, `:209`). No single-layer arm has ever run (CORPUS/37–39, 44 F-A2: 5-, 9-, 2-layer sets). Add **B0**: all 24 facts at one fixed layer (modal ℓ*, else 8) through the same wrapper. Without it a B gain reads "one layer vs spread"; a B loss hides a per-fact effect. Cost: one arm.

2. **Criterion (b).** Derivation checks: one layer, cache 0, `upd = (A⁻¹PKRᵀ)ᵀ` (`:209–211`), so `upd k_i = Σ_j r_j G[j,i]`, `P` symmetric (`:175`). But "fraction returned" is exact only along r_i; the realised fraction ⟨Δh, r_i⟩/‖r_i‖² also carries Σ_{j≠i} G[j,i]⟨r_j, r_i⟩/‖r_i‖², which *is* target-dependent — "one map for A1/A7" holds for the diagonal only, and `Σ|G[j,i]|` (`C10V:32`) is not the cross-talk that matters. For n = 1, Sherman–Morrison gives `G = ‖P_ℓ k_i‖² / (1 + ‖P_ℓ k_i‖²)`: the argmax is where the key's null(C) component is largest against an absolute ridge `L2 = 1.0` (`:28`) and absolute `NULL_THRESH = 0.005` (`:29`, `:174`), neither scale-normalised across layers. Expect the map to track per-layer scale: one layer for most facts (stop fires) or hair-width variation (noise). Pre-register a margin δ (ℓ* counts only if `G_ℓ*[i,i] − G_runner-up ≥ δ`) and report `‖P_ℓ k_i‖` per cell.

3. **Descending order (c) — premise right, consequence omitted.** `compute_ks` and `cur` are forward reads at layer ≤ the group layer (`repr_tools.py:31–40`; `compute_z.py:214–216`; `my_edit:196–201`); a layer-ℓ edit alters only deeper activations. But shallower groups' ΔW act on every token's `down_proj` input, so deep-group facts' layer-ℓ keys in the evaluated model are no longer the pristine `k_i` their solve assumed; the engine's ascending loop recomputes `cur` after each edit to absorb exactly that (`memit_main.py:152–169`). State the trade, and add the readout that tests the premise: **post-edit realised fraction per fact in the composed model** (Δh at the keyed position against r_i, one forward pass).

4. **Stop rules (d).** "≥ 20/24 same" needs item 2's margin. "Map not reproducible" demands exact in-process argmax agreement (`C10V:36`); MPS noise flips near-ties — use the margined map. Templates are resampled per process (CORPUS/44 F-A4), so the gate-A map will plausibly differ; running the published map (`C10V:60`) is right, but cross-process agreement /24 must be reported.

5. **LAW#5 audit (e) — insufficient.** The gate at `:463` runs with the map `None`, so only the delegate path is tested; the one-layer path (`hp_ℓ`, `P[ℓ − 4]`, override keys `(subject, " " + value)` — `req` stores `" " + targ`, `:97`, matching `c10q:50`) is never checked numerically, and counters cannot catch a wrong projector index. Fix: one request, map `{s → 8}` through the wrapper against `my_edit` with `layers = [8]` on the original path, the engine's own z in the override; ΔW relative distance against an in-process floor (`C10S:28`).

6. **Arm C cache (f).** A non-zero cross-group cache makes the group solve differ from the lone write `G` describes, with no engine analogue (`C10V:51`). Zero the cache per group as in B; drop the copy-back. ℓ† = ℓ* + 1 also makes `z_layer ≠ ℓ*` (`:184`).

7. **Spread paths (g).** Gaps: (i) LEAD-LARGE-WRITE contradicts H-V1's "same write size" — state it does not pass gate A; (ii) the whole-residual write is up to 5× arm A's per-layer residual (`:204`), so a strength effect is live — B0 is the control; (iii) `"{s} is a"` is the solve's KL prompt (`C10S:22`), so that probe is anchored by the objective — keep it, label it.

8. **Minor.** Whether A1 realises more than A7 at the keyed position was never measured — **UNVERIFIABLE** (no A1 ρ_c in CORPUS/44); one step-0 line would say whether realisation is the A7-specific wall at all.

**Drift.** Advances the live step-4 lead on the §C write path; not a §0.3 falsifier; the NULL-is-not-closure scoping (`C10V:9`) is right.
