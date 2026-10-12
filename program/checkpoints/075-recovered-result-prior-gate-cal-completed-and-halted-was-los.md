## RECOVERED RESULT — prior GATE-CAL completed and HALTED (was lost to a disconnect)
A prior session's GPT-J GATE-CAL **completed** (json written 01:27, preserved as `s241_gatecal_gptj.prior_0127.json`) with:
- `null_floor_JS = 0.0985` → **floor_near_zero = False** (threshold <0.02)
- `counterfact_JS = 0.3748`, `destructive_ceiling_JS = 0.389` (ceiling ordering holds), `kl_factor_monotone = True`
- **VERDICT = `HALT-floor-not-clean`**
Meaning: even a NULL/identity MEMIT edit (re-assert the model's current top-1) perturbs same-entity OTHER attributes (~0.0985 JS) — the metric has no clean ~0 floor on GPT-J. Per the plan this is a HALT (harness/metric needs a deeper look) AND is itself evidence for same-entity non-locality. Per CLAUDE.md a clean HALT is SUCCESS.
The current durable run (PID 49432) **REPRODUCES the HALT** (per-fact, observed live):
- NULL floor: Eiffel 0.0203 / MJordan 0.0649 / Curie 0.2450 → mean ≈ 0.110 (vs prior 0.0985; Curie's degenerate null target ' the' dominates) → floor NOT clean.
- COUNTERFACT: Eiffel 0.462 / MJordan 0.380 / Curie 0.317 → mean ≈ 0.386 (vs prior 0.3748).
- DESTRUCTIVE (mom2/10): Eiffel 0.460 / MJordan 0.387 → ≈ COUNTERFACT, i.e. same-entity drift already near-ceiling at normal edit strength (thin floor→ceiling band).
- Cross-entity JS ≈ 0 throughout (lineage control clean).
Gate VERDICT locked = HALT (null_js 0.110 ≮ 0.02). Current run = clean reproduction of prior_0127 HALT. When it finishes, its `gate` block overwrites `s241_gatecal_gptj.json` (prior preserved at prior_0127).
**Next decision (for operator/next session):** GATE-CAL HALT on GPT-J → do NOT promote to Phase 1 until the null-floor is understood. Options: (a) accept ~0.0985 as the GPT-J same-entity noise floor and re-scale "local vs corrupted" relative to it (floor/ceiling/destructive give the band); (b) investigate why a null edit drifts (MEMIT re-solve perturbation even at zero target delta); (c) run Qwen GATE-CAL for its floor before deciding. Plan §Phase0 GATE language: floor must be ≈0 on BOTH models else HALT.

