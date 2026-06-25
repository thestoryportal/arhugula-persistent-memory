---
name: pool-sizing-levers-items-then-determinism
description: "Power-sizing clustered editing trials — clusters=orderings; spend held-out-probes first, then determinism; CORE=1.0 is a rule-of-three rare-event test, not an effect-size test"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb61dcd0-ac28-4e0b-a2b3-805299505b73
---

When sizing a clustered editing-trial pool with `tools/power.py` (2026-06-24, F1 stimulus pool; `docs/F1_STIMULUS_POOL_SIZING.md`, `results/f1_pool_sizing.jsonl`):

- **A power.py "cluster" = one independent edit-ORDERING (a GPU edit run), NOT a seed×order cell.** The `--cluster-sd`/`--swing` you pass IS the between-order variance, so the unit it counts is the ordering. Held-out **seeds evaluated on the same edited model are cheap eval ≈ more *items*, not clusters** — reading "12 clusters = 4 orders × 3 seeds" triple-counts correlated evals and is anti-conservative. Cost driver = orderings = GPU edits.
- **Lever order: spend the cheap lever first, then the expensive one.** (1) **Held-out probes per ordering** is nearly free (extra eval on an edit you already paid for) and dominates at low counts: items 8→16→32 cut required orderings 19→12→9. (2) **Determinism** (cutting between-order swing) is the ONLY lever on the expensive orderings axis and dominates *once items are saturated*: at items=32, swing 5→15→50 ⇒ 7→9→16 orderings; at items=8 the same swing move was only 19→23 (binomial noise masked it). So [[clustered-design-power-determinism-cheaper-lever]] is right but conditional — determinism's payoff appears after you've maxed the items lever.
- **Continuous margins are ~4× more powerful per ordering than binary** (3–5 vs 9–19 here) → recast every near-ceiling test (e.g. R5 native-firing) as a firing-margin, not binary top-1 ([[match-metric-to-the-claim]]).
- **A CORE=1.0-EXACT gate is a rule-of-three rare-event test, NOT an effect-size test.** ~300 clean probes bound failure <1%, ~3,000 <0.1%. A 20pp-effect sizing answers the *bystander/magnitude* question only; size the exact-1.0 gate separately and carry BOTH probe populations in the pool ([[resolve-the-gates-real-criterion]]).
- **Don't lock the count to a 3-ordering swing estimate** — re-estimate swing from the first ~5 real orderings and re-size; verify between-held-out-set variance is small (else seeds become a real middle level, not free eval).

**Why:** got the cluster-unit and the lever-ordering claim checked by advisor before writing the pool spec; the central "determinism dominates at high items" claim was untested until I ran the items=32×swing cell it demanded.
**How to apply:** for any future pool/run sizing in this program (C1/C3/C2/C4, D20-grid, B3), size with power.py FIRST; maximize probes/ordering, minimize orderings via determinism, use continuous metrics for ceilings, and rule-of-three any exact-1.0 gate.
