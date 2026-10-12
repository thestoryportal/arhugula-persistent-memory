# 15 — A2 RELATION-BALANCED IN-SOLVE SENTINELS (the runtime-incremental cross-entity fix)

_Result 2026-06-18. Track-A follow-up to G6.1 (`CORPUS/13`) and A1 (`CORPUS/14`). Pre-registered in `EXPERIMENT_RUNBOOK.md` §8 A2. Artifacts: `a2_relbal_sentinels.py`, `a2_relbal_sentinels_result.json`, `a2_relbal_sentinels.log`; stimulus `g6_screen_qwen3b_v2.json` (78-entity expanded screen). Engine UNMODIFIED; LAW#5 gate-1 (engine vs harness MEMIT) INERT (Δexpr=0.0019) and gate-2 (sentinel λ_s=0 ≡ alphaedit, code-path identity) IDENTICAL (Δexpr=0.000000)._

## The question
A1 showed **batch** (Genesis) is cross-entity clean; the **sequential / runtime-incremental** path is still corrupted (A0/G6.1: held-out edited-relation top-1 collapses to ~33–42% at N=100). A2 tests the principled fix: add held-out **same-relation sentinel keys** `K_S` to the preservation term **inside each sequential solve** — "address = relation + ENTITY" (LARQL), an extension of the D20 orthogonal-projection mandate. Does it prevent cross-entity read corruption while keeping write-side wins?

## Design (3 disjoint pools, anti-tautology §2.3)
Seeded shuffle (seed=0) of the 78-entity v2 screen → **edit(50) / sentinel(10, protected) / eval(10, measured, never edited or protected)**, all disjoint (asserted), drawn from one distribution (removes the append-order confound; gives the eval pool test power). N=100 = 50 edit entities × 2 fields (capital, language), sequential, `cache_c` accumulating. Sentinel keys built once from the clean base. λ_s swept {0, 0.5, 1, 2, 5}; λ_s=0 = code-path-identity control. Eval edited-relation axis = **20 probes (10 entities × 2 relations) → 5%/probe.** Eval baseline: edited_rel 100% correct, continent 90% (stable control).

## VERDICT — PARTIAL (strong, directional): sentinels substantially mitigate but do not eliminate

**Eval held-out edited-relation top-1 correct (counts /20, the binding metric):**
| | N=26 | N=50 | N=100 | retention@100 | within-JS@100 |
|---|---|---|---|---|---|
| λ_s=0 (control) | 16/20 | 15/20 | **8/20 (40%)** | 100% | 92.5% |
| λ_s=0.5 | 19/20 | 19/20 | 15/20 (75%) | 93% | 85.5% |
| λ_s=1.0 | 19/20 | 18/20 | 16/20 (80%) | 95% | 86.0% |
| λ_s=2.0 | 19/20 | 19/20 | **17/20 (85%)** | 92% | 88.1% |
| λ_s=5.0 | 19/20 | 19/20 | 15/20 (75%) | 85% | 84.3% |

- **The robust signal** (far outside the 5%/probe resolution): control **8/20 → sentinels 16–17/20** at N=100 — a **+8–9-probe lift**. Sentinels roughly halve the cross-entity read corruption.
- **Resolution honesty:** the λ fine-structure (peak "at λ_s=2", "drop at λ_s=5") rests on 1–2 probe flips on the eval axis = single-run noise. The claim is **"λ_s≈1–2 is a usable middle,"** NOT "λ_s=2 is optimal." Do not lock a λ_s.
- **No PASS:** no λ_s reaches the pre-registered bar (eval ≥95% AND retention ≥95% at N=100). Best balanced: λ_s=1.0 (16/20 eval, 95% retention) / λ_s=2.0 (17/20 eval, 92% retention).

### The robust trajectory (stronger than any single N=100 point) → A3
**Every sentinel arm still DECLINES N=50→N=100** (λ_s=2: 19→19→17; λ_s=1: 19→18→16) and **within-entity JS declines monotonically** (50 probes, λ_s=2: 96.3→94.4→88.1%). Sentinels **slow the onset and raise the floor** of the corruption; they do **not arrest** it. Extrapolated past N=100 it keeps falling. Mechanism (advisor, matches research consensus): protecting 10 sentinel entities' keys pins the **shared relation direction** (hence the +8–9 lift), but a **residual entity-specific component** beyond that direction is not pinnable by a few keys → needs a leakage-aware solve (A3 BetaEdit) or a basis change (A6 SAE), not more sentinels.

### The λ wall (real on retention/within, NOT eval)
Increasing λ_s past ~2 over-constrains the solve: **retention falls 95→85%** (over 100 records = 1%/record → a real 10-record drop) and within-JS falls — both on many-probe axes, so robust. On eval, λ_s=5's "75%" is 2 probes of noise; the wall is read off retention/within, not eval.

## Controls & integrity
- **Both inertness gates passed**; gate-2 (λ_s=0 ≡ alphaedit) was bit-exact (Δexpr=0.000000) → the sentinel code path is the proven AlphaEdit path plus a vanishing term at λ_s=0.
- **λ_s=0 control collapses** (16→15→8/20) ≈ A0's sequential collapse → the test has power; the recovery at λ_s>0 is real, not a floor artifact.
- **Apply-time expression = 100% at every λ_s and N** → no false-no-op (the new v2 edit entities express; the Llama trap is avoided).
- **Relation-specific:** continent (unedited relation) `stable_vs_pre` = **100% at every λ_s** → sentinels/edits corrupt the edited relation only, not other relations (the 90% continent "correct" is stable baseline knowledge).

## Caveats (kept flush — none block the PARTIAL→A3 fork)
- **Single seed (seed=0), single ordering, 3B, one run.** The qualitative verdict survives one run (the +8–9-probe lift ≫ noise), so the *fork* is safe; but a *locked λ_s* would need seed replication we don't have → the decision is directional only.
- **Sentinels cost within-entity locality too** (λ_s=0→2 at N=100: within-JS 92.5→88.1%) — a second trade beyond retention.
- **Fixed clean-base `K_S`:** sentinels protect W·K_S against the *clean-base* keys while W drifts under 100 edits → the constraint goes stale as N grows, which could itself contribute to the N=100 falloff. → **A2b (recompute K_S per rung)** is the cheap next probe (below).
- Eval edited-relation axis is 20 probes (5%/probe); read counts, not fine % differences.

## Forks & decisions
- **FORK (§8 A2): PARTIAL → A3** (BetaEdit leakage-aware solve, may close the residual via pseudo-null-leakage compensation; sentinels may stack on top) **and/or A4** (mid-late band may give the edit more non-shared room). **Plus A2b first** (cheap).
- **A2b — NEW, cheapest-informative (advisor), run before the BetaEdit port:** recompute `K_S` per rung (or per edit) so the sentinel constraint tracks the drifting W instead of going stale. Cov-reusing one-liner on `a2_relbal_sentinels.py`. If stale-K_S is the limiter, A2b closes more of the gap for free; if not, the BetaEdit port (A3) is earned.
- **D-A2-1 ⟨D-A2-1@f26b823b⟩ (directional):** relation-balanced in-solve sentinels are a **partial mitigation** of runtime-incremental cross-entity corruption (subject-keyed AlphaEdit, Qwen2.5-3B) — ~halve it (8→17/20 @N=100), at a retention/within-entity cost, with an over-constraint wall past λ_s≈2 — **not a complete fix.** Not locked into the recipe pending A2b + A3 + seed replication.
- **Spec ripple:** D20 should note sentinel preservation **helps but is insufficient alone** for high-fan-out relations at scale; the complete in-weight fix (if any) needs leakage-aware solving or a basis change, else the spec adopts the hybrid read-path (A5). OQ-W1 reframing (Track D) stands.
