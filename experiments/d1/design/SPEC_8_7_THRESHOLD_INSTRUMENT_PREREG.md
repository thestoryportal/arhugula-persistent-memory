# §8.7 Numeric-Threshold Instrument — Pre-Registration (lower-variance read-corruption instrument)

_Created 2026-06-21 (task #9). Pre-registration for the **lower-variance instrument** that the numeric §8.7 per-relation-concentration WARNING/HARD thresholds block on. Extends `docs/B1_SIZE_TERM_PREREG.md` + `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md` §4.5. **Criteria FROZEN before any GPU run** (DISCIPLINE §2.6 / runbook §2.3). Decision `D-D1-2` (numeric threshold + instrument)._

_DRAFT until: (1) `advisor()` design pass — **DONE 2026-06-21** (redirected the threshold basis + the validation gate; see §9); (2) operator review (launch the cheap diagnostic). Then frozen — no post-hoc threshold edits (§3.1)._

---

## 0. F1 link — what this closes

The §8.7 **structural** amendment (per-relation `max_relation_concentration_since_anchor` drives `drift_tier`) is D1-final and model-general (D1 + B1 7B replication). The one open sub-item for F1 is the **numeric value** of the per-relation WARNING/HARD thresholds — OQ-W1. B1 showed the **sequential held-out-corruption instrument is ~50pp run-to-run nondeterministic on a bit-identical config** (7B seed3 k36: 4.2%↔41.7%), so the existing instrument **cannot set a quantitative threshold**. This pre-reg builds + validates a lower-variance instrument and, if it validates, reads the first numeric threshold off it (on Qwen2.5-3B).

**Deliverable for F1:** either (a) a numeric per-relation-concentration threshold curve `corruption(k)` with bounded uncertainty on ≥1 deployed model, stated in operational read-corruption terms — or (b) a pre-registered honest negative ("even a continuous metric + Monte-Carlo + determinism cannot stabilise this instrument; the threshold is irreducibly trajectory-chaotic → §8.7 must use a conservative spread-based rule, not a mean-crossing"). Both are F1 inputs.

---

## 1. Root-cause model of the 50pp variance (two distinct sources)

The B1 50pp swing was on a **same-seed, bit-identical config** → the only differing input is **nondeterministic GPU kernels**. But a second amplifier sits on top:

- **Source A — GPU/cuBLAS nondeterminism** compounding over 24–48 sequential edits (each edit reads the current corrupted weights via `compute_z`/`compute_ks`, so noise accumulates along the trajectory).
- **Source B — the cliff amplifier.** Binary top-1 correctness is a hard threshold on a *continuous* margin (correct-token logit − top-distractor logit). After corruption, many held-out entities pile up near margin≈0, so a tiny logit perturbation flips many at once → the binary % is chaotic near the cliff, independent of how noisy the underlying logits are.

The instrument attacks **B first** (it is the larger, always-present amplifier and the pool caps held-out at ~30, so a binary count is intrinsically coarse) and treats **A** as a nuisance to characterise, not necessarily to eliminate.

## 2. Threshold basis (advisor-redirected — the load-bearing design decision)

> **The §8.7 threshold is set from the MEAN + SPREAD (or a conservative high quantile) of a CONTINUOUS read-quality metric as a function of per-relation concentration k — NOT from a single deterministic realization.**

Rationale (advisor, §9): a deterministic run picks one draw from a distribution **deployment will itself sample from** (real edits run on nondeterministic kernels). A deployment threshold wants `E[corruption | k]` or a conservative quantile. Moreover **the run-to-run spread is itself deployment-relevant signal** — a concentration where corruption is 20%±50pp is unsafe regardless of the mean — so WARNING/HARD may be defined partly by *where the spread blows up*, not only where the mean crosses a level. Forcing determinism (`Var=0` by construction) would throw that away. **Determinism is therefore demoted to nuisance-control / exact-repro / size-term enabler, and is explicitly NON-load-bearing** (§5): if it proves an infra firefight, the continuous-metric + Monte-Carlo path stands alone.

### 2.1 Continuous metrics (the low-variance backbone)
Per held-out **baseline-correct** capital entity, after each measurement point, log on the gold capital-token:
- **`margin`** = logit(correct) − max logit(other) — the smooth backbone (PRIMARY continuous metric).
- **`nll`** = −log p(correct) (mean over held-out) — smooth, avoids prob saturation (raw prob piles at 0/1; the action is the mid-range → use NLL/log-prob/margin, not mean prob — advisor).
- **`rank`** = rank of the correct token (1 = top-1).
- **`top1_correct`** (binary) — retained as the **operational** read-corruption metric (a query returns the wrong city) the spec ultimately cares about.

Report `mean ± SD` over held-out entities AND over runs/seeds for every metric at every k.

## 3. The instrument-validation gate (advisor-redirected — run FIRST, cheap, the real gate)

The B1-style "two deterministic runs agree" check is **near-tautological** (it only confirms determinism is *on*, which the preflight already checks) and is NOT used. Replaced by the **repeat-variance diagnostic**, which is the decisive cheap experiment and the operator checkpoint:

**DIAGNOSTIC (Phase 0, run before any fine-grid sweep):**
1. Pick the most unstable known operating point: **the config that swung 50pp** (7B seed3 k=36; if 7B VRAM/time is heavy, 3B at its own most-corrupted mid-k — chosen from a quick 1-seed 3B staircase — with the choice logged before the repeats).
2. Repeat that fixed config **N_REPEAT=5× WITHOUT determinism**. Record run-to-run **SD** of: `top1_correct` (binary) AND each continuous metric (`margin`, `nll`, `rank`).
3. Repeat it **2× WITH determinism**; overlay the deterministic point(s) on the non-deterministic spread.

**Pre-registered reading (frozen):**
- **WORLD 1 — `SD(continuous)` is small (margin SD ≤ ~10% of its clean-vs-corrupt dynamic range) while `SD(top1)` is large (≥ ~20pp):** the binary cliff was the whole problem. **→ continuous metric + seed CIs suffices; determinism is optional polish.** Proceed to the fine-grid sweep on the continuous metric.
- **WORLD 2 — `SD(continuous)` is also large:** genuine weight-trajectory chaos. **→ the threshold MUST be reported as a Monte-Carlo `E`/quantile over R≥5 nondeterministic runs per k (with CIs); a deterministic point would be actively misleading.** Proceed, but every k gets R repeats (cost ↑ — re-scope grid/model with operator).
- **Overlay check:** record where the deterministic draw sits in the non-deterministic distribution (central / extreme). If extreme → confirms (A) would have been wrong; documents it.

This gate does NOT have a HALT branch on "noise too high" — high residual noise is a *finding* (World 2 → spread-based threshold), not a failure. It HALTs only on infra error (determinism unfixable AND continuous metric still chaotic enough that even R=10 gives CIs too wide to separate WARNING from HARD — reported as the honest-negative deliverable §0(b)).

## 4. Fine-grid concentration sweep (the threshold curve — after the gate)

**Primary curve:** the **pure-capital staircase** — k = capital-edit-count = exactly the §8.7 `max_relation_concentration_since_anchor` axis. Held-out same-relation read quality `corruption(k)` measured at a **fine k grid**: `k ∈ {0,6,12,18,24,30,36,42,48}` (resolution to locate the onset/knee, vs B1's 3-point {24,36,42}).
- Each k: restore clean → apply k sequential capital edits (counterfactual reassignment, in-solve AlphaEdit, band[4-8], thresh 0.005, L2=1.0 — recipe FROZEN, identical to D1/B1, NOT re-tuned) → measure all §2.1 metrics on the disjoint held-out pool.
- **Seeds:** ≥3 (entity-draw sampling CIs). **Repeats per k:** R=1 in World 1, R≥5 in World 2.
- **Held-out:** grow to pool max (≤30 with TOTAL edit pool 48; the continuous metric is the variance fix, not held-out count). Note: screen-expansion (>78 entities) is an optional future lever, not in scope here.
- Log **cumulative band-summed ‖ΔW‖_F** per edit (B1 §2.1) so the curve can be read against edit-strength, not just edit-count.

**Conservatism arm (anti-anti-conservative — advisor):** the pure-capital staircase is **anti-conservative** — D1's non-negative cross-relation term means realistic *mixed* inter-anchor load corrupts *more* at the same capital-k. So at the chosen threshold k\*, **spot-check** held-out capital corruption under a **realistic mixed load** (capital-k\* + additional other-relation edits to a realistic inter-anchor total). The shipped threshold must be **at or below** the pure-capital knee, validated by the mixed-load spot-check — never read off the pure curve as if it were the safe ceiling.

## 5. Determinism = nuisance-control, NON-load-bearing (infra pass)

`torch.use_deterministic_algorithms(True)` + `CUBLAS_WORKSPACE_CONFIG=:4096:8` + seed-all (torch/cuda/numpy/python). **Preflight (cheap, before Phase 0):** enable it, run the LAW#5 inertness gate + a 2-edit sequential mini-schedule; catch the first op without a deterministic CUDA kernel (candidates: attention → try `attn_implementation="eager"`; scatter/`index_add` in the weight write; `linalg.solve`/`eigh` → CPU fallback already used for the solve in the alphaedit path). **One-fix-then-halt per op; if determinism cannot be made to run cheaply, DROP it** — the continuous-metric + Monte-Carlo path (World-2 mode) does not need it. Determinism is used for: exact repro, the overlay in §3, and (bonus) finally making the 3B-vs-7B size term resolvable.

## 6. Operational threshold definition (pre-registered BEFORE the sweep — anti-Goodhart)

The §8.7 thresholds are stated in **operational read-corruption** terms (top-1, since a query returning the wrong city is the deployment harm), located robustly via the continuous curve + spread:
- **WARNING (proposed):** the per-relation concentration k at which **held-out same-relation top-1 corruption first exceeds 5%** (mean over held-out+seeds) **OR** the run-to-run spread first exceeds ±10pp (whichever k is *lower* — conservative), validated ≤ the pure-capital knee and confirmed by the mixed-load spot-check.
- **HARD (proposed):** k at which **top-1 corruption exceeds 20%** mean **OR** spread exceeds ±25pp (lower k wins).
- These 5%/20%/±10pp/±25pp operational levels are **FROZEN here, before the sweep**. They derive from "what read-error rate makes the DB untrustworthy for a query," NOT from any observed number. The *output* is the concentration k mapping to each level (with CI), per model.
- If World 2 dominates (spread never tightens), the deliverable is the **spread-based rule** ("WARNING at the k where ±spread first exceeds ±10pp") — an honest, still-actionable threshold form.

## 7. Pass/fail (FROZEN)
- **INSTRUMENT-VALIDATED:** Phase-0 diagnostic completes and assigns World 1 or World 2 (both are valid outcomes; both yield a usable threshold form). Continuous-metric clean-vs-corrupt dynamic range is non-degenerate (margin separates clean from highest-k by ≥ its own pooled SD), positive control fires (highest-k corrupts), expression ≥95% on edited facts.
- **THRESHOLD-DELIVERED:** the fine-grid sweep yields k\* values for WARNING/HARD (per §6) with CIs that **separate** WARNING from HARD (non-overlapping at ±1 SD). Reported with the mixed-load conservatism check.
- **HONEST-NEGATIVE (a real result, §0b):** CIs too wide to separate WARNING from HARD even at R=10 → report the irreducible-chaos finding + the conservative spread-based rule; do NOT fabricate a point threshold.
- **INVALID (not a result):** expression <95% in any arm; LAW#5 gate fails (|Δ|≥0.05 → HALT); positive control fails to corrupt at highest k (continuous metric flat → instrument can't see the effect → debug, do not report a threshold).

## 8. LAWs / gates (runbook §2.4)
1. **Engine fingerprint** — SHA of `memit/memit_main.py` = 5c0c706a…; `grep -c _cov_cpu == 3` for the wide-intermediate (7B) arm.
2. **LAW#5 inertness** — `my_edit` "memit" mode reproduces stock `apply_memit_to_model` (|Δ|<0.05) on this harness before any science result; re-run after the determinism patch (the patch must be proven inert: deterministic-mode toggle changes NO science tensor).
3. **Read-source-before-authoring** — harness is the proven B1 port (`experiments/track_b/b1_size_dose_response.py`); the continuous-metric + determinism additions are **measurement/runtime-flags only**, science path VERBATIM. `cat`-read any op before a CPU-fallback patch.
4. **One-fix-then-halt** on any harness/determinism bug; HALT + diagnostic JSON to `architecture_profile/`.
5. **Storage discipline** — no deletes outside §3.3; results to `results/`, never only `/dev/shm`.

## 9. Advisor design pass (2026-06-21) — applied
- **Fork resolved → (B):** threshold basis = mean+spread/quantile of a continuous metric; determinism NOT a valid threshold basis (one arbitrary draw from a distribution deployment samples) and destroys the deployment-relevant spread signal. **Determinism demoted to nuisance-control, non-load-bearing.** (§2, §5)
- **Validation gate replaced:** the "two deterministic runs agree" gate was near-tautological (only confirms determinism is on). Replaced by the **repeat-variance diagnostic** (5× non-deterministic + 2× deterministic overlay), run FIRST, World-1/World-2 discrimination + operator checkpoint. (§3)
- **Continuous metric:** prefer **margin / NLL / log-prob** over raw prob (saturates; action is the mid-range). (§2.1)
- **Pure-capital staircase is anti-conservative** (D1 cross-term): set threshold ≤ pure-capital knee + **mixed-load spot-check**. (§4 conservatism arm)
- Unchanged: 3B first; pure-capital staircase as the primary curve; pre-register operational top-1 levels before the sweep.

## 9b. Cross-family review (gpt-5.5 via Codex, 2026-06-21) — DESIGN REVISED PRE-NUMBER
Independent out-of-family adversarial review (`logs/codex_review_threshold_OUT.log`), run AFTER the Phase-0 diagnostic + a single-draw sweep but BEFORE any threshold number was computed/written. **Verdict: "not yet justified"** as designed. It **diverges from the Opus advisor on the primary metric** and supplies a stronger estimator. Reconciliation (evidence-led, not authority-led):

- **Primary metric = BINARY top-1 corruption, NOT the margin curve (Codex overrides Opus).** Tie-breaker is definitional: the spec's harm is "a query returns the wrong city" = top-1. Margin can hide a few entities flipping catastrophically while the mean stays acceptable. **Margin/rank/NLL demoted to diagnostics + smoothing cross-check** (preserves Opus's variance concern). Supersedes §6's margin-led knee + §2 "threshold basis = continuous metric" for the *threshold definition* (continuous still the low-variance diagnostic backbone).
- **Estimator = per-k Wilson/Beta-binomial UPPER CONFIDENCE BOUND on binary corruption, pooled over runs; threshold = earliest k where UCB crosses the level.** Replaces §6's "earliest-k-of-worst-case" (min/max of a tiny sample is an artifact). **Report all three: observed-worst, UCB-conservative, margin-inflection** — nothing hidden.
- **Frozen levels UNCHANGED: WARNING=5%, HARD=20%** (set in §6 before any data). Only the *estimator* and *metric basis* changed, on independent-methodology grounds, before the final number — documented here for pre-registration integrity. Discreteness made explicit: held-out=24 → 1 wrong=4.17%, 2=8.33%, 5=20.83% ⇒ WARNING@5% ≈ "≥2/24 wrong."
- **Sampling unit = the ORDERED edit subset, not just seed/process.** `edit_pool[:k]` jaggedness is real entity-specific interference. → add a **focused low-k (k=4–14) randomized-edit-ORDER replication set** (the decision region), not high-k confirmation. (Live confirmation: seed-3 across-process at k=8 gave 0% vs 8.3% corruption — the WARNING point is process-unstable; ΔW-norm was identical ⇒ cliff-crossing, not norm variance.)
- **Determinism = diagnostic only** (one repro pair), not the canonical instrument — deployment path is batch-clean; this governs the A3-parked incremental path.
- **Pure-capital anti-conservatism = serious** (both reviewers): measure a mixed-load condition before shipping a general number, OR label narrowly "pure same-relation capital-only incremental; mixed-load untested."

**Net design (reconciled):** matrix (across-process + across-seed, all k) **+ focused low-k randomized-order set** → threshold from **Wilson-UCB on binary top-1** at the frozen 5%/20% levels (report observed-worst/UCB/margin too) → **mixed-load spot-check** before any general claim → ship a **conservative, narrowly-scoped** number with the discreteness + scope caveats. Independence obligation (DISCIPLINE §3.1) now SATISFIED for this artifact (Opus advisor + gpt-5.5 cross-family).

## 10. Artifacts (planned)
Harness `experiments/track_d/d1_threshold_instrument.py` (port of `b1_size_dose_response.py` + §2.1 continuous metrics + repeat/determinism flags; science path VERBATIM). Phase-0 diagnostic result `results/d1_instrument_variance_diagnostic.json`; fine-grid result `results/d1_threshold_curve_{3b,7b}_result.json`. Writeup folds into `CORPUS/22` + `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md` §4 (replaces "OPEN" with the numeric curve or the honest-negative). Decision `D-D1-2`. Close-out: `python3 tools/closeout_check.py D-D1-2` → ✅ ALL GREEN.
