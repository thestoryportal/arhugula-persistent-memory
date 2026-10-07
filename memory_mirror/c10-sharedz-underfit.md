---
name: c10-sharedz-underfit
description: "CORPUS/51 (D-C10s-sharedz, 2026-10-06): one target fit jointly over three phrasings (step 1, H-1) stayed below the 0.98 fit on 18 subject-frame entries within the engine's 25-evaluation budget → UNDERFIT, inconclusive; the write arm did not run; the 51 → 69/72 injection count is an unedited-model observation, not a write result."
metadata:
  node_type: memory
  type: project
---

Step 1 of the research-pass sequence (D-C10s-sharedz@bee04393). The first inertness run halted on checks (iii)/(iv) (0d422ad) because they compared fp16 batches of different shapes; the operator ruled D-C10r-rulings-6 (fix the two over-strict checks, rerun step 1, then the location control; seal the held-out questions from the loop agent). Amendment A2 v1 (looser tolerances) was withdrawn after both reviews; A2 v2 made the unmodified engine build the same batch (parity 0.0) and added a same-process noise twin (+3). The rerun was ALL INERT, and the fit veto fired before the screen.

**Why:** UNDERFIT is pre-registered as "inconclusive under this solve budget; nothing concluded about frames". The partially fit shared target injected into the unedited model scored 69/72 against the canonical 51/72, but CORPUS/46 F-D1 shows injection in the unedited model does not predict the edited model.

**How to apply:** never cite 69/72 as a write result or as a LEAD. Per prereg §3 the sequence moves to step 2 (D-C10t-secondkey). A fixed-frame solve-feasibility follow-up (larger iteration budget at the current radius first; change a solve constraint, never the 0.98 criterion) is a candidate only — the operator decides whether it runs before step 2. Batch-shape fp16 rounding moves the engine's own target (rel 0.0977, 7 vs 19 rows): compare solves at the same batch shape. See [[c10-stacked-solve-tradeoff]], [[research-pass-2026-10-06-sequence]].
