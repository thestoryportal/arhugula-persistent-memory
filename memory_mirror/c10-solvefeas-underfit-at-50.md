---
name: c10-solvefeas-underfit-at-50
description: "CORPUS/52 (D-C10s-solvefeas, 2026-10-07): step 1's shared target re-solved with the solve cap 25 → 50 evaluations → UNDERFIT-AT-50, objective-stopped; 29 → 2 failing fit entries in the same run, the two left stop early on the engine's averaged loss rule; write arm not run; 72/72 is an unedited-model injection observation."
metadata:
  node_type: memory
  type: project
---

Follow-up of step 1 (D-C10s-solvefeas@7083a102), run under D-C10r-rulings-7 (2) and the overnight standing approval D-C10r-rulings-8. One change only: the solve cap 25 → 50 evaluations; frames, held-out set, radius, KL/weight-decay and the engine's verbatim stopping rule fixed. Valid and ALL INERT; the per-frame 0.98 fit gate still fails on 2 entries (Plurnak T2, Vorlex T2), both stopped at evaluation 27 because the averaged total loss fell below 0.05 before every frame reached 0.98.

**Why:** the averaged loss rule is not an all-frame guarantee, so raising the cap again would keep the same early stops. Iterations did contribute (27 of 29 failing entries repaired in the same run), but this is not the pre-registered budget outcome. Injection counts (canonical 54 vs shared 72/72, twin +2) are on the unedited model; CORPUS/46 F-D1 says that does not predict the edited model.

**How to apply:** never cite 72/72 as a write result, a pass or a LEAD; never compare 18 → 2 across CORPUS/51 and CORPUS/52 as causal (different context draws; the paired evidence is this run's 29 → 2). Next per prereg = step 2 (D-C10t-secondkey) carrying the canonical target. A fit-guarded early stop (each frame ≥ 0.98 plus the averaged rule; register H-C10s-fitguard) is a candidate only and departs from the engine's verbatim rule — own prereg, review and inertness controls. See [[c10-sharedz-underfit]], [[research-pass-2026-10-06-sequence]].
