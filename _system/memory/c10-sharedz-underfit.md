---
name: c10-sharedz-underfit
description: "HISTORICAL (2026-10-06/07): CORPUS/51-52 shared-z UNDERFIT at 25 and 50 evaluations; never cite the 69/72 or 72/72 injection counts as write results."
metadata:
  type: project
---

Step 1 of the research-pass sequence (D-C10s-sharedz@bee04393). The first inertness run halted on checks (iii)/(iv) (0d422ad) because they compared fp16 batches of different shapes; the operator ruled D-C10r-rulings-6 (fix the two over-strict checks, rerun step 1, then the location control; seal the held-out questions from the loop agent). Amendment A2 v1 (looser tolerances) was withdrawn after both reviews; A2 v2 made the unmodified engine build the same batch (parity 0.0) and added a same-process noise twin (+3). The rerun was ALL INERT, and the fit veto fired before the screen.

**Why:** UNDERFIT is pre-registered as "inconclusive under this solve budget; nothing concluded about frames". The partially fit shared target injected into the unedited model scored 69/72 against the canonical 51/72, but CORPUS/46 F-D1 shows injection in the unedited model does not predict the edited model.

**How to apply:** never cite 69/72 as a write result or as a LEAD. Per prereg §3 the sequence moves to step 2 (D-C10t-secondkey). A fixed-frame solve-feasibility follow-up (larger iteration budget at the current radius first; change a solve constraint, never the 0.98 criterion) is a candidate only — the operator decides whether it runs before step 2. Batch-shape fp16 rounding moves the engine's own target (rel 0.0977, 7 vs 19 rows): compare solves at the same batch shape. See [[c10-stacked-solve-tradeoff]], results/research_pass_2026-10-06/HANDOFF.md.

**Follow-up, CORPUS/52 (D-C10s-solvefeas, 2026-10-07; merged from c10-solvefeas-underfit-at-50):** the shared target re-solved with the cap 25 → 50 evaluations → UNDERFIT-AT-50, objective-stopped; valid and ALL INERT; 29 → 2 failing fit entries in the same run, the last two (Plurnak T2, Vorlex T2) stopping at evaluation 27 because the engine's averaged loss fell below 0.05 before every frame reached 0.98 — the averaged loss rule is not an all-frame guarantee, so raising the cap again keeps the same early stops. Never cite its 72/72 (unedited-model injection) as a write result, pass or LEAD; never compare 18 → 2 across CORPUS/51 and /52 as causal (different context draws; the paired evidence is that run's 29 → 2). A fit-guarded early stop (H-C10s-fitguard) departs from the engine's verbatim rule and needs its own prereg, review and inertness controls. (Both routings above were executed: step 2 = CORPUS/53.)
