# 16 — A2b REFRESH-K_S (is sentinel-key staleness the A2 limiter?)

_Result 2026-06-18. Track-A follow-up to A2 (`CORPUS/15`) and A1 (`CORPUS/14`); pre-registered in `EXPERIMENT_RUNBOOK.md` §0.3/§8 A2b, advisor-upgraded before authoring. Artifacts: `a2b_refresh_ks.py`, `a2b_refresh_ks_result.json`, `a2b_refresh_ks.log`; stimulus `g6_screen_qwen3b_v2.json`. Engine UNMODIFIED; LAW#5 gate-1 (engine vs harness MEMIT) INERT (Δexpr=0.0030) and gate-2 (sentinel λ_s=0 ≡ alphaedit, code-path identity) IDENTICAL (Δexpr=0.000000)._

## The question
A2 added held-out same-relation sentinel keys `K_S` to the in-solve preservation term, halving the runtime-incremental cross-entity corruption but **not arresting the N50→100 decline** (`CORPUS/15`). `K_S` was built **once from the clean base** and reused in all 100 sequential solves. A2b asks the cheapest possible follow-up before the BetaEdit port: **as W drifts under 100 edits, does the clean-base `K_S` go stale, and is that staleness itself driving the decline?** If yes → refreshing `K_S` closes the gap for free (cov-reusing). If no → the residual is something sentinels can't reach → BetaEdit (A3) earned.

## Design (advisor-upgraded to be decisive, not single-seed directional)
- **3 seeds × λ_s∈{1,2} × {FIXED clean-base `K_S` control, REFRESH per-edit `K_S`}**, all four arms run in **one script, same seed/λ** (no cross-run confound — the FIXED arm is the in-script control, NOT A2's stored JSON).
- **REFRESH = per-edit** (`REFRESH_EVERY=1`, the max-refresh arm; per-edit `build_Ks`=0.67s, feasible) → recomputes `K_S` against the current drifted W before each solve. Per-edit is the strongest version: if it doesn't help, no coarser schedule would.
- **Isolation:** only `K_S` varies. P (clean-base, AlphaEdit design) and `cache_c` (accumulating edited keys) held — so the conclusion is scoped to `K_S`.
- **Mechanism logged for free:** per-layer `K_S` drift (relative-Frobenius + mean column-cosine, clean-vs-current) at every rung, both arms.
- **Pre-registered noise-aware verdict** (anti-anchor, derived from the FIXED arm's own variance): STALENESS-MATTERS iff mean_seeds(refresh−fixed)@N100 > SD_seeds(fixed)@N100. The eval edited-rel axis is 20 probes (5%/item), so a 1–2 item move is noise — single-seed cannot separate staleness from seed.

## VERDICT — K_S STALENESS RULED OUT as the A2 limiter (3-seed paired + clean seed-0 instrument)

**As-coded noise-aware verdict (`correct_vs_truth`@N100):**
| λ_s | FIXED [s0,s1,s2] | REFRESH [s0,s1,s2] | meanΔ | SD_fixed | verdict |
|---|---|---|---|---|---|
| 1 | [95, 80, 85] | [70, 90, 90] | −3.3 | 6.24 | RULED-OUT |
| 2 | [90, 70, 80] | [90, 80, 85] | +5.0 | 8.16 | RULED-OUT |

Both |Δ| < SD_fixed → staleness not established.

**Metric correction (advisor — match-metric-to-the-claim).** `correct_vs_truth` is confounded by per-seed eval baselines (seed 0/1/2 pre-edit correct = 100/50/40%): editing can flip eval reads *toward* truth. `stable_vs_pre` has the **opposite** confound in low-baseline seeds (e.g. seed-2 FIXED λ1: correct 40→85 while stable→30 = the **same reads flipping to correct**, miscounted as instability). **Only seed 0 (100% baseline) is a clean corruption instrument** — there any flip = corruption, and stable==correct exactly (95/95, 90/90). Two metric-robust reads both rule staleness out:
- **Clean seed-0 instrument:** FIXED 95/90 (λ1/λ2) vs REFRESH 70/90 → refresh ≤ fixed (no help; λ1 *worse*).
- **Paired within-seed Δ** (bias cancels — both arms share the eval pool, so it survives the confound in all 3 seeds): λ1 = [−25, +5, 0] mean −6.7; λ2 = [0, 0, 0] mean **0.0**. Refresh ⩽ 0 everywhere.
- **Retention cost:** refresh slightly *hurts* (λ1 meanΔ −3.3) or flat (λ2 +0.3).

**The decisive dissociation:** `K_S` drift was **large** in seeds 1 & 2 (mean column-cosine fell to 0.83 / 0.80; seed 0 stayed 0.996), yet per-edit refresh that tracked that drift produced **zero corruption improvement**. This is not the ambiguous "drift was negligible so refresh couldn't matter" — it is "we removed substantial staleness and it still didn't help." → the residual is **not** a `K_S`-staleness artifact.

## Scope of the claim (kept tight)
- **Measured:** refreshing the sentinel keys `K_S` against current W does **not** reduce runtime-incremental cross-entity corruption (3-seed paired + clean seed-0), and slightly costs retention. **"K_S staleness ruled out" — NOT "refresh doesn't help" in general.**
- **NOT tested here:** BetaEdit's **P-refresh** (refresh the *projection matrix*, history-aware) and its full-rank **`λ1·Σ`** leakage term are *different objects* — both untested. A2b refreshed `K_S`; BetaEdit refreshes P.
- **Inference (not a measurement):** that the residual is the **entity-specific component beyond the shared relation direction** — supported by (refresh-didn't-help) + the G6.1/synthesis mechanism, but it is an inference.
- **Corruption magnitude** is characterized on the clean seed-0 instrument only; do **not** anchor A3's success bar on beating seed-1/2 `stable`≈30% (inflated by counting toward-truth flips as corruption). A3 must screen the eval pool to confident-correct pre-edit (G6.1-style) so its instrument is clean across seeds.

## FORK → A3 (BetaEdit), now a PORT not a reimplement
The entity-specific residual needs the principled, full-rank, leakage-aware approach. **The official BetaEdit repo was found this turn** (`lbq8942/BetaEdit`, IJCAI 2026; cloned to `external_prior_art/BetaEdit`; ships a `qwen2.5-3b` config = our exact band[4-8]/`mlp.down_proj`/`subject_last`/wikipedia setup, on the same MEMIT primitives as our engine). Its solve = our AlphaEdit solve **+ `λ1·Σ`** (full-covariance leakage penalty in the LHS) **+ τ-periodic history-aware P-refresh**. This **retro-explains Track A**: A2's `λ_s·K_S·K_Sᵀ` is a **low-rank shadow of BetaEdit's full-rank `λ1·Σ`** (a handful of sentinels ≈ rank-≤20 sample of the relation manifold's second moment) — which is exactly why A2 was PARTIAL. A2b shows the cheap door (cycling the same low-rank stand-in) is closed; A3 opens the principled one. A3 = **port the solve into our inertness-gated harness, re-tune for the N=100/base-model regime** (their `λ1=3000, λ2=10, τ=1000, thresh=0.02`, Instruct, `mom2=15000` are tuned for gpt2-xl @ 10k edits — `τ=1000` never fires at N=100; copy the math, derive the constants). LAW#5 gate: BetaEdit at `λ1=0, τ>N, λ2=L2` reduces bit-exactly to our current AlphaEdit (advisor-verified against `betaedit_main.py:265-270`).

## Scope check carried to the operator (HIL)
A1 (`CORPUS/14`) already shows **batch / Genesis ELIMINATES** this corruption (held-out edited-rel top-1 flat 100→100→100% @ N≤100). A2/A2b/A3 only matter if deployment requires **incremental online single-fact writes**. If periodic batch-rebuild of the overlay is acceptable, A3 is optional polish on an already-solved problem. **Confirm incremental writes are a hard requirement before the port.**
