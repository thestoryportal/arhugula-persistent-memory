# F1 Stimulus-Pool Sizing — the design decision

**Date:** 2026-06-24. **Status:** DECISION (sizing complete; pool BUILD is the next, operator-effort step).
**What this is:** the ungated closure-path step 1 from `docs/F1_DETERMINATION.md` §4 — size the large-N stimulus pool that gates the three sharpest open conditions (**C1** compaction-at-scale, **C3** R5-at-scale, **C2** read-contract scale legs) *before* building it, so those runs can actually falsify rather than produce underpowered noise.
**Instrument:** `tools/power.py` (simulation-based, cluster-level Welch t; self-tests PASS 2026-06-24). Raw results: `results/f1_pool_sizing.jsonl`. Inputs anchored on measured D20 data (`CORPUS/23`).

---

## 1. The sizing grid (every number is **orderings per arm**, not seed×order)

⚠ **Read "clusters" as independent edit-ORDERINGS.** The `cluster-sd` fed to power.py *is* the between-order swing → each power.py "cluster" is one ordering = one GPU edit run. **Held-out seeds are NOT clusters** — evaluated on the same edited model they are effectively more *items* (cheap eval), which is exactly why the items lever works. Cost driver = orderings = GPU edits. (Advisor-confirmed; the anti-conservative "12 = 4 orders × 3 seeds" reading is wrong.)

| Test | metric | p0/m0 | effect | items/order | swing (pp) | **orderings/arm** |
|---|---|---|---|---|---|---|
| C1 bystander-magnitude | prop | 95% | 20pp | 8 | 15 | **19** |
| C1 bystander-magnitude | prop | 95% | 20pp | 16 | 15 | **12** |
| C1 bystander-magnitude | prop | 95% | 20pp | **32** | 15 | **9** |
| C1 bystander-magnitude | prop | 95% | 20pp | 32 | **5** | **7** |
| C1 bystander-magnitude | prop | 95% | 20pp | 32 | **50** | **16** |
| C1 (smaller mid-range effect) | prop | 95% | 10pp | 16 | 15 | 14 |
| C3 R5 native-firing (binary, near-ceiling) | prop | 98% | 15pp | 16 | 15 | **23** |
| C2 read-contract margin | cont | 0.55 | 0.30 | 10 | csd 0.08 | **3** |
| C2 read-contract margin | cont | 0.55 | 0.20 | 10 | csd 0.08 | **5** |

## 2. Three quantified design levers

1. **Held-out probes per ordering is the dominant CHEAP lever.** items 8→16→32 cuts C1 from **19→12→9** orderings/arm. Adding probes costs only extra *eval* queries on an edit run you already paid for — nearly free. **Decision: ≥32 held-out probes per relation per ordering.**
2. **Determinism (cutting between-order swing) is the only lever on the EXPENSIVE orderings axis — and it dominates once items are saturated.** At items=32, swing 5→15→50 moves **7→9→16** orderings/arm (2.3×); at items=8 the same swing move was only 19→23 (1.2×, binomial masks it). So: spend the items lever first, *then* invest in determinism to shrink the orderings count. ([[clustered-design-power-determinism-cheaper-lever]], now quantified for this design.)
3. **Continuous metrics are ~4× more powerful per ordering than binary.** C2's margin metric needs **3–5** orderings vs C1's binary **9–19**. **Decision: recast every near-ceiling test as a continuous margin** — R5 native-firing as a firing-margin (not binary top-1) drops it from ~23 into the 3–5 regime ([[match-metric-to-the-claim]]).

## 3. ⭐ C1 is TWO statistical questions — the pool must carry both

The sizing above answers the **bystander/held-out magnitude** question (does sub-batched compaction reintroduce a ~20pp read-corruption in the held-out population — the G6.1 signature the spec's CompactionProbeReport is blind to). It does **NOT** size the spec's actual CORE gate:

- **CompactionProbeReport gates CORE retention = 1.0 EXACTLY** (§8.10; any CORE regression aborts). That is a **rare-event / ceiling** test, not a 20pp-effect test. **Rule-of-three:** to bound CORE-failure < 1% you need ~**300** clean CORE probes; < 0.1% needs ~**3,000**. ([[resolve-the-gates-real-criterion]].)

→ The pool needs **two distinct probe populations**: (a) **bystander/held-out magnitude probes** (≥32/relation/ordering, the §2 sizing) and (b) a **rule-of-three-sized CORE probe set** (≥300, scale toward 3,000 for a strong gate) graded for exact-1.0.

## 4. POOL BUILD SPEC (the deliverable for the next, operator-effort step)

Build a large-N stimulus pool with:
- **Entity set across all 5 relation families** (§7.3 Structural/Knowledge/Constraint/Taxonomy/Namespace) at large N, **with concentration C variable independently of total N** — this is what breaks the D20 **K-vs-C confound** (the open requirement for C1's 2D N×C grid).
- **Importance tags CORE / SUPPORTING / INCIDENTAL** (§8.6); the **CORE subset rule-of-three-sized** (≥300, target 3,000) for the exact-1.0 gate.
- **≥32 held-out probes per relation per ordering** (magnitude lever); **2–3 held-out seeds** to start (see caveat 5.2).
- **Reverse-pairs** (for C2/R2 reverse-lookup falsifier — the reversal-curse).
- **Multi-token values** (for C10 multi-token robustness; the whole base is currently short-value).
- **High-confidence uncommitted-but-known negatives** (for R5 leak / closed-world channel).
- **Continuous-margin instrumentation** on every probe (firing margin / JS), so ceiling tests use the powerful metric.

**Working orderings target:** **~9–12 orderings/arm for C1** (items=32, swing=15, 20pp) — *provisional, pending the swing re-estimate (5.1)*. R5 binding at ~23 *if left binary* → recast to margin and it drops to ~3–5.

## 5. Caveats baked into the design (do not lock numbers prematurely)

1. **swing=15 is a 3-ordering estimate** from D20's 3B between-order spread (the parameter that *sets* the orderings count). **Re-estimate it from the first ~5 real orderings and re-size** before committing the full grid. Determinism work (reducing swing) directly buys back orderings (50→5 nearly halves them).
2. **The seeds≈items mapping assumes between-held-out-set variance (beyond binomial) is small.** Verify with 2–3 seeds on the first ordering; if set-variance is large, held-out seeds become a *middle* variance level needing their own count (not just free eval).
3. **GPU cost is real.** orderings × N×C grid-cells × 2 arms (clean vs sub-batched). E.g. 10 orderings × a 4×3 N×C grid × 2 arms ≈ **240 edit runs** = many hours on the single 4090. Within standing infra auth ([[standing-auth-forward-requirements]]) — narrate it; **if the grid is wide, the grid breadth is a one-line scope call for the operator.**
4. Scope of these numbers: Qwen2.5-3B / band[4-8] / AlphaEdit / the D20 corruption regime. They size the 3B falsifiers; 7B (C4) inherits the larger ~50pp swing → expect the high end of the orderings range there.

## 6. Status / next

- **Pool SIZING: DONE** (this doc; `results/f1_pool_sizing.jsonl`). Ungated, no GPU.
- **Pool BUILD: NEXT** — operator-effort (authoring the large-N tagged stimulus set per §4). The one operator-facing scope call: **grid breadth** (how wide the N×C grid + how many orderings → directly sets GPU hours).
- Then: C1 compaction-at-scale (2D N×C grid, single-joint-solve to N→2,000, CORE=1.0 gate, COMPACTION_ABORTED) leads, emitting C3's R5 seam metrics in the same factorial; C2 ungated read legs in parallel.
