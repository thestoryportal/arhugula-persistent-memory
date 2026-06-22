# F1 Comprehensive Runbook — evidence the spec across ALL layers (executable)

**Date:** 2026-06-22. **Status:** LIVE — the ready-to-execute runbook for the re-grounded program. **Full rationale + reviews:** `REGROUNDING_PLAN_v2.md` (plan + §9 reconciliation), `REGROUNDING_COUNCIL_SYNTHESIS.md` (6-domain council), `REGROUNDING_PLAN_FOR_COUNCIL.md` (Advisor+Codex v1). De-dup: this runbook = the executable critical path + live state; rationale lives in those docs, cited not restated.

## North star (unchanged)
F1 — prove/falsify the LLM-as-Database spec is implementable across ALL layers, **outcome-level** (spec mechanism OR an evidenced equivalent), at a **committed stated scope**. Falsification-first. **CARVE-OUT:** security/authz/audit/provenance clauses are NOT outcome-equivalence-eligible (mechanism + red-team + architectural proof required).

## Two-phase shape (operator-decided)
- **Phase 1 (GPU priority) = the MEMORY-CONTRACT SUBSTRATE** — which database obligations the model/weights can carry vs which require the `.vindex`/Git/governance overlay. Two co-equal leading edges (read contract + compaction-at-scale) + write-engine SENTINELS, on a shared stimulus pool. "Co-equal" = co-DESIGN; the single 4090 serializes heavy GPU runs by information value.
- **Phase 2 = governance/protocol** (2PC/TC/Ledger/breaker · Auth-Gate/token/audit/red-team · orchestrator/lock-hold/queues · Pruning/GC + reconciliation), built ON the Phase-1 seam emissions. Deferred, fed by the binding seam register (`REGROUNDING_PLAN_v2.md` §4).

## Evidence is TYPED (the matrix selects the tool per requirement)
`empirical-falsifier` (universal/reliability) · `constructive-demonstration` (existential/capability — "demonstrate proven", ONLY for "works at one scoped point") · `threshold-calibration` (quantitative) · `fault-injection / state-machine` (protocol) · `red-team + architectural-proof` (security invariant) · `comparative` (in-weight vs RAG vs hybrid) · `compositional/integration-invariant` (write→compact→delete→quantize→read). Every row carries a "what result makes this FAIL" column; PROVEN-FOR-SCOPE invalid without its full scope tuple.

## ⭐ Medium-of-Obligation Table (anti-scope-laundering — Codex D1; authored BEFORE experiments)
Every Database-Behavioral-Contract row is tagged `WEIGHTS_MUST_CARRY | VINDEX/GIT_MAY_CARRY | GOVERNANCE_MAY_ENFORCE | HYBRID_ALLOWED | OUT_OF_SCOPE`. Every PASS/PARTIAL/FAIL cites it. If a capability works only via an external index/verifier, the verdict reads "hybrid passed; weight-native X **unshown**" — never a laundered pass.

| Contract row | Medium (current) | Basis |
|---|---|---|
| **Read: closed-world SELECT (value for committed, null for absent)** | **HYBRID_ALLOWED at best; weight-native UNSHOWN** | B0 pilot (2026-06-22): separation is edit-margin-driven + leak channel live → needs external commit-status bit. Loops to B3N. |
| Read: native-knowing / reason-over-fact (fact fires in inference) | WEIGHTS_MUST_CARRY (candidate) | the paradigm payoff (§G/line 90); untested as L2 behavioral probe |
| Write: batch genesis store, corruption-clean | WEIGHTS_MUST_CARRY | A1 (now re-graded constructive-at-one-point) |
| Update/Delete: deletion non-resurfacing | TBD | untested |
| Provenance / commit-status / deletion-tombstone | **GOVERNANCE_MAY_ENFORCE** (non-retrofittable bit; must be minted Phase-1) | Warden C6; B0 leak confirms no weight-native commit bit |
| Authorization / audit (Gate, token, ledger) | mechanism required (NOT outcome-equiv) | Warden C5; G2 verifier PROVEN-FOR-SCOPE |
| _…remaining rows authored during spec-first extraction…_ | | |

## PHASE-1 CRITICAL PATH (live state)
1. **B0 — SELECT-primitive go/no-go — ✅ DONE (2026-06-22).** `docs/B0_SELECT_PRIMITIVE_PREREG.md` · `results/b0_select_primitive_pilot.json` · `results/B0_RESULT_ANALYSIS.md`. **Verdict:** mechanical OUTCOME-A but CONFOUNDED — committed read-back 8/8@0.997 is **edit-margin inflation**; the one un-confounded signal is the **LEAK channel** (uncommitted-but-known facts read correct 6/6 @ 0.43–0.82 → no weight-native commit-status bit). Honest lean → toward OUTCOME-B. SELECT/closed-world is HYBRID-at-best. **GO on Edge B, but the question is now the crossing test (step 2), not a pool build.**
2. **B1 (reframed) — the LEAK-SURVIVAL CROSSING TEST — ⏸ HELD FOR OPERATOR GREENLIGHT.** Falsification-first single test: **committed margin under (quantized + scaled) conditions vs. leak ceiling over deliberately HIGH-confidence uncommitted-known facts.** Cross → weight-native closed-world read is DEAD; SELECT = `GOVERNANCE_MAY_ENFORCE` only (a substantive F1 finding). Prior = "can a hybrid gate be rescued from a likely-negative." Not auto-run (sharper/different than originally scoped). **Operator question: run B1 next, OR fold the B0 leak finding straight into the F1 read-contract determination (may already be decisive).**
3. **Stimulus pool V0/V1** (operator-approved infra) — built only AFTER B0/B1 resolve; serves both edges: large-N + closed-world ground-truth (two negatives: fictional + real-uncommitted) + reverse-pairs + 5-relation-family + CORE/SUPPORTING/INCIDENTAL tags.
4. **Edge A — compaction-CORE-at-scale** (top risk-ranked falsifier; already directional-negative D20): probe the **bystander** population (not just declared edges — the spec's CompactionProbeReport is blind there); 2D N×C grid (break K-vs-C); single-joint-solve to N→2,000; CORE retention EXACTLY 1.0; exercise COMPACTION_ABORTED + the liveness wedge. Leads the heavy GPU runs.
5. **Write SENTINELS** (de-scoped from co-equal): W1 capacity ceiling = curve-design + one sentinel; W2 general-capability regression = thin held-out delta attached to large runs. Full characterization → Phase 1b only if B0/compaction survive.

## Seam register (binding — co-equal deliverable; full list `REGROUNDING_PLAN_v2.md` §4)
Behavioral (L1-SELECT/L2-INFER split, online drift predictor, compaction heal/abort, negatives/conflict/deletion-resurfacing, isolation/rollback-invisibility, quantized-query-equivalence) · capture-now timing (compile/compaction wall-clock @2,000, mount-window read-block) · discriminator bits (provenance/commit-status/deletion-tombstone — non-retrofittable, mint in Phase 1).

## Findings re-validation = RE-GRADE + DEMOTE (not presence-check; `REGROUNDING_COUNCIL_SYNTHESIS.md` §6)
A1 batch-clean → constructive-at-one-point (tightens B3N — re-examine decisions built on it, not just the finding); G3 Validation → constructive-demo; T2.5/A5 compaction-regression → MIS-TARGETED (no bystander/CORE=1.0/importance); CP2 "L1 SELECT delivered" → at-risk (intent-index, not deployed store); k≤1 → keep as fail-closed SENTINEL; G2 Security → PROVEN(verifier mechanics) but NOT red-teamed.

## Build method
Spec-first, layer-by-layer requirement extraction into the Database-Behavioral-Contract matrix (+ Medium-of-Obligation tag + evidence-type + "what makes this FAIL"). Template experiment-DESIGN on Read; findings-re-grade on Write. Pre-register can-fail criteria + advisor + gpt-5.5 at each promote gate; close-out gate per promoted result.

## Open operator decisions carried
(a) B1-next vs fold-leak-into-F1 (above); (b) when to start the spec-first full-matrix extraction (the comprehensive requirement enumeration across all 9 layers — the remaining bulk of "comprehensive").
