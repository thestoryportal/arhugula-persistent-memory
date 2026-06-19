# 20 — C2 / RELATION-INCLUSIVE KEYING + KEY-COLLINEARITY DEPTH MAP

_Result 2026-06-18. Track-C run, root-cause probe of the G6.1 cross-entity corruption (`CORPUS/13`). Pure measurement (no edits, no covariance) — `compute_ks` activations only. Artifacts: `experiments/track_c/c2_key_collinearity.py`, `experiments/track_c/c2b_depth_map.py`; results `results/c2_result.json`, `results/c2b_depth_map_result.json`; logs `logs/c2_phase0.log`, `logs/c2b_depth_map.log`. Engine UNMODIFIED. Decision: **D-C2-1**._

## The question
G6.1 cross-entity bleed (same-relation, cross-entity) is driven by **collinear keys**: the `down_proj`-input activations of capital(France), capital(Italy)… overlap, so a rank-1 edit at one bleeds to the others. The corpus identified a candidate no-engine-patch fix (workaround-b): key at a **relation-inclusive** position (subject `"France's capital"`, template `"{} is"` → `subject_last` lands on the "capital" token) to separate the keys. C2 tests whether that actually reduces same-relation key collinearity — BEFORE any expensive edit run.

## VERDICT — C2 PRUNED; a mechanism map emerges

**Phase-0 (relation keying):** relation-inclusive keying makes same-relation keys **far MORE collinear**, not less:

| band | SUBJECT-key cos | RELATION-key cos |
|---|---|---|
| L4 | 0.68 | 0.93 |
| L6 | 0.67 | 0.94 |
| L8 | 0.26 | 0.94 |

Keying at the "capital" token collapses every entity onto the shared relation direction (cos 0.93–0.99). It would make cross-entity bleed **worse**. **C2 is pruned** — the corpus workaround-(b) hope was wrong for the cross-entity problem (it may help same-entity multi-field, a different problem A1's batch already solves).

**C2b (depth map, subject keying):** same-relation key collinearity is **U-shaped in depth** (reproducible across capital AND language):

| band | key cos (capital / language) |
|---|---|
| L2–6 (early) | 0.57–0.70 |
| **L8–12 (mid)** | **0.20–0.42** ← most separable |
| L16–22 (the spec's C15 range) | 0.73–0.78 |
| L24–28 (late) | 0.88–0.91 ← most collinear |

## What this resolves, and what it does NOT
- **RESOLVES:** relation-inclusive keying is eliminated. Late-band editing (A4) **for cross-entity isolation** is eliminated (late layers are *more* collinear). Converts the program's standing "shared-relation-direction" *inference* into a **measured, layer-resolved quantity**.
- **NEW spec tension (C15):** the spec's edit band **L15–25** sits exactly where same-relation keys are highly collinear (0.73–0.78) — mechanistically the **worst** zone for cross-entity isolation. A real tension between "where edits take/generalize" (C15, late) and "where keys separate" (mid, L8–12); a new axis on the CP3 C15-divergence (`CORPUS/09`).
- **NEW lead:** our band **[4-8]** dilutes the separable L8 (0.26) with collinear L4–6 (0.68–0.70). A band on the separability sweet spot **[8–12]** might reduce *sequential* cross-entity corruption at the root — a testable fix (needs cov for L9–12).
- **DOES NOT resolve:** whether key-collinearity *causally* drives cross-entity bleed. It is a **plausible mechanism, not yet causally tested** — [4-8] batch is clean at 3B despite collinear L4–6 (the joint solve absorbs it), so the link matters for the **sequential/incremental** path. A band-[8–12] sequential run vs [4-8] would test it.

## Caveats (kept flush)
- 12 same-relation entities; Qwen2.5-3B only; subject-keyed AlphaEdit context.
- Collinearity is a **proxy** for bleed, not the bleed itself — the causal link is the open question above.
- A4 (mid-late band [18-22]) is eliminated *for the isolation rationale*; it may still matter for C15/expression (a different criterion).

## Decision
**D-C2-1:** Relation-inclusive keying PRUNED (cheap negative). The mechanism is now measured: same-relation key separability is maximal at **L8–12**, minimal in the C15 late band. Next root-cause experiment, if pursued, is **band [8–12] sequential** (gated on cov for L9–12), not keying and not late-band. Feeds the C15 reconciliation (OQ-W2) and D1.

## FORK
PRUNED → keying is not the lever. Two live continuations: the **B3/E3 L2-necessity decision** (if in-weight is not required, the incremental cross-entity problem is moot) and the **band-[8–12] mechanism test**. See `docs/HYPOTHESIS_REGISTER_2026-06-18.md` C2/C3/D1/D2.
