# Pre-registration — D-C10s-solvefeas: step 1 again with a larger solve budget (H-C10s-solvefeas) (v2, 2026-10-06 ~23:45)

**Status: v2 — the advisor's v1 review (`results/c10s_solvefeas_advisor_v1.md`, FIX-FIRST, 4 BLOCKING) folded; for implementation by Codex, then the advisor's implementation review, before any run.** Decision-ID `D-C10s-solvefeas`. Operator ruling D-C10r-rulings-7 (2): before step 2, run a pre-registered solve-feasibility follow-up of step 1. Codex recommended step 2 first; the operator chose this (`results/c10s_sharedz_codex_verdict.md` item 4). Parent: CORPUS/51 ⟨D-C10s-sharedz@bee04393⟩ (UNDERFIT). This arm **does not relabel CORPUS/51**.

## 0. Where this sits, and what it can conclude
The same cell as step 1: the §C write path, compile step, target definition, read against the §8.9 bar. In CORPUS/51 every shared solve stopped on the 25-evaluation budget. The seven underfit facts were all still falling at the stop: per-evaluation NLL ratios Oxbarrow 0.62, Zephquin 0.54, Fluvane 0.68, Marsduq 0.75, Drennik 0.83, Crulpane 0.82, Skornwell 0.86 (advisor v1, recomputed from `results/c10s_sharedz_r2/inject.json`). Three explanations were left open: (a) too few steps at the current radius, (b) the radius or the KL/weight-decay trade-off, (c) tension among the three frames under one displacement. This arm tests (a). Context templates are sampled unseeded per process, so a comparison with CORPUS/51's numbers is across template draws. **The binding before/after comparison is therefore inside this run** (§2). Nothing here closes the frame hypothesis.

## 1. The one change, everywhere
`v_num_grad_steps` 25 → **50**, through `configs/hparams/qwen25_3b_memit_hparams_steps50.json`, identical to `qwen25_3b_memit_hparams.json` except for that key. Why 50: following each underfit fact's recent slope, about 3–5 more evaluations reach 0.98, and about 10–15 allowing for the slowdown the well-fit facts show; 50 gives roughly double that headroom. The KL and weight-decay terms alone were ≥ 0.05 at evaluation 25 in 22 of 24 solves, so most solves will run all 50 evaluations; the stopping rule rarely ends one early. Hitting the clamp does not rule out more steps helping: the solves kept improving along the clamp boundary.

**One budget for every solve and every arm**: the canonical target (engine `compute_z`), the shared target, the noise twin, the inertness checks and the harness pass (A1, A2, the reference A7 and the shared A7). The harness takes one settings object per recipe, so it cannot split them anyway. The only canonical-vs-shared difference stays the phrasings. Everything else in `docs/C10S_SHARED_Z_PREREG.md` v3 + A1 + A2 v2 applies unchanged: the forms, the held-out set, the overlap rule, the inertness checks (i)–(v) as amended, cell 1 with control c and the twin, the screen rule, the 0.98 fit bar, the stopping rule verbatim, the clamp radius 0.75, cell 2, §3's labels and gates, and the second process.

## 2. The same-run snapshot at evaluation 25 (the binding before/after)
The step count only sets the loop bound and the final break (`compute_z.py:108,167`), so in a 50-evaluation solve the state at evaluation 25 (before its update) is exactly the 25-step solve's final state in the same process. The shared solve records **per-prompt NLL at every evaluation**, plus the frame fits and `delta` at evaluation 25. Cell 1 also injects the **evaluation-25 shared z** on the held-out templates, recorded beside the final one but not gated: a same-run, same-template reproduction of step 1's cell 1.

## 3. Readings (exact; frozen with this document; the rules live in the reader)
Each (fact, frame) entry below 0.98 at the stop is classified as:
- **objective-stopped**: the solve ended by the engine's total-loss rule (< 0.05) with this frame below 0.98. The engine's averaged objective was satisfied: neither the budget nor (b)/(c).
- **plateaued**: its frame fit changed by less than 0.002 between evaluations 40 and 50.
- **still-descending**: otherwise.

Labels:
- **BUDGET-BINDING** (fit gate passes at the stop, and at least one entry was below 0.98 at evaluation 25 in this run): the budget was the binding constraint in this run. The screen, the write arm and §3 of the step-1 prereg follow, read with the write gates, -LARGE-WRITE and the second process. A LEAD or PARTIAL is a step-1 result at a 50-step budget, and the record says so.
- **FIT-PASSES-AT-25** (the gate already passes at evaluation 25 in this run): the template draw, not the budget, separates this run from CORPUS/51. Recorded as such; the screen and write arm still follow, under the same reading.
- **UNDERFIT-AT-50**, qualified by the classes present: with only plateaued entries, the budget alone does not repair the fit, which points at (b) or (c) without separating them; with still-descending entries, the budget is not exhausted as an explanation; with objective-stopped entries, the averaged objective, not the budget, ended the solve. Next is step 2 in every UNDERFIT case.
- **NOISE-NON-DISCRIMINATING**: as A2.
- **REFERENCE-SHIFT**: the pass's reference A7 at 50 steps lands outside the identical-baseline envelope [5, 18]/72 or canon [5, 10]/24. That is a finding about the budget's effect on the canonical edit, not an INVALID: HALT the arm, record it, report it. A1, A2 ≥ 68 stays a validity gate.
The reader prints each failing entry's evaluation-25 fit beside its final fit. Ten entries passed at only 0.980–0.985 in CORPUS/51, so a small template-draw shift can move an entry across the bar. In every case the injection counts are recorded beside CORPUS/51's, and nothing changes CORPUS/44–51.

## 4. Plumbing that must hold (advisor v1 items 2–4)
- **A closed arm selector, not a free path:** `C10S_ARM` ∈ {`sharedz` (default; behaviour exactly as at `1169794`), `solvefeas`}. It sets together: the Decision-ID, the prereg path, the halt path (`architecture_profile/c10s_solvefeas_halt_diagnostic.json`; the step-1 halt file must never be written by this arm), the settings file, and the expected step count.
- **The settings reach every solve.** The driver rebinds `hp` from the arm's settings file and asserts `hp.v_num_grad_steps`; `HP_CANDIDATE` is set before the harness import; the inertness script uses the same `hp`. Every record names the settings path actually used, its sha256 and the step count; `H.HP_BASE` is no longer written as if it were the settings in use.
- **Bound across processes:** the inertness record carries the arm, the settings sha256 and the step count; `require_inertness` and the `second` stage refuse any mismatch, so a 25-step inertness record cannot certify a 50-step run.
- **Engine solves counted:** a read-only forward hook counts the model's forward passes around every engine `compute_z` call (one per evaluation) for the canonical, twin and harness solves, so each recorded target states how many evaluations it ran. Positive control: at least one solve in the run ran more than 25 evaluations; otherwise the arm is INVALID.
- Both prereg docs and the new settings file join the hashed source list. With `C10S_ARM` unset, the selftest and an equality check show behaviour identical to `1169794`.

## 5. Cost and order
Cell 1 ≈ 50–60 min; cell 2 ≈ 45–60 min if it runs; a second process ≈ 45–60 min more if a PARTIAL or LEAD needs it. It runs after the location-control rerun (one GPU run at a time). Halt discipline and close-out as the step-1 prereg §5, with this arm's own halt path.
