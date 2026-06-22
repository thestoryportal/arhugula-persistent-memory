# Re-Grounding Plan — Framework Council Synthesis (facilitator)

**Date:** 2026-06-22. **Inputs:** the 6 domain specialists (MEMIT · Graph/Query · State · Validation · Warden · Orchestration), each grounded in CORPUS/05 + spec sections under COUNCIL_PROTOCOL, building on the cross-family Advisor (Opus) + Codex (gpt-5.5) reviews. **Status:** advisement on the DRAFT plan (`REGROUNDING_PLAN_FOR_COUNCIL.md`), NOT evidence. Council = spec-contract framing; leads, not proof.

## Headline
The council endorses the plan's direction (typed evidence, Database-Behavioral-Contract spine, binding seam register) but finds **both structural moves are too clean**: (a) "Read co-equal / Write just re-grade" *over-corrects* — Write has 3 unresolved hard gates; and (b) "defer all governance to Phase 2" *leaks* — several governance properties are model-coupled, capture-now, or non-retrofittable and MUST be instrumented in Phase 1. The seam register is therefore not a side-list; it is a co-equal Phase-1 deliverable.

## Convergent findings (multiple domains, independently)

### C1 — The SELECT-vs-INFER gap is the read contract's BLOCKER (Graph + Validation, both #1)
The program has only ever read via **INFER (generation)**. CP2 found LARQL `SELECT FROM EDGES` cannot read back even a native fact as a triple. The plan lists "§8.9 post-write probe" as one seam but never (a) commits to demonstrating a **structured SELECT primitive distinct from free-form INFER**, nor (b) splits the **L1 write-verification SELECT** from the **runtime query-surface SELECT**. Without this, "Read co-equal Phase-1" measures INFER's eloquence, not a database query surface — **the prototype-tautology trap one level up.** This gates whether the read contract is evidenceable at all.

### C2 — Negative reads = the lead/meta-falsifier (Graph; echoed Codex)
If the model confabulates a plausible answer for an absent key (LLM default; the reversal-curse's cousin), then every *present*-key PASS is also untrustworthy. Absent→non-null must be the **first** read falsifier, scored as a **confabulation rate**, not one seam among many.

### C3 — Compaction-CORE-retention-at-scale is the top whole-system spec-killer (State + Orchestration + MEMIT)
- **Sampling-frame gap in the spec itself (State):** §11.14 `CompactionProbeReport` samples **declared edges** (CORE/SUPPORTING/INCIDENTAL) only; D20 corruption lands on **cross-entity bystanders** → the spec's own CORE=1.0 heal-gate would PASS a compaction that silently corrupted un-edged knowledge. Must probe the **bystander population**.
- **Liveness, not just corruption (State):** compaction-abort → anchor never resets (§8.7) → drift never clears → HARD trigger at 8,000 suspends writes → READ_ONLY **wedge**. "Compaction is the heal" failing = a liveness failure of the drift/anchor/circuit-breaker machine.
- **Already directional-negative (MEMIT/D20):** vs the read contract which is a coverage hole (never-tested, not yet failing). Needs the larger screened stimulus pool + 2D N×C grid (K-vs-C) + single-solve-at-true-scale.
- **Orchestration nomination:** the #1 risk-ranked falsifier by "which single failure invalidates the most contracts at once" — kills C-OC3 (CORE gate) + C-OC2 (atomic compaction) + B3N condition-3 + the memory-lifecycle loop the orchestrator exists to govern.

### C4 — Write Engine is NOT "done, just re-grade" (MEMIT)
Three clauses are unresolved, not re-gradeable, all gated on the **larger screened single-token stimulus pool the plan never commits to build**: (1) capacity ceiling as a **number/curve-to-breaking-point** (the plan's "scope envelope" *dodges* this by picking a safe N); (2) **general-capability forgetting at scale** (the literal other half of "model-as-memory-layer" — no matrix row asks "is the base still a working model after 100s–1000s of edits"); (3) compaction **Component-1 SCALE**. Promote the stimulus pool to a Phase-1 infrastructure deliverable; schedule 3 write-engine hard gates co-equal with Read.

### C5 — Outcome-equivalence is UNSAFE for security/authz/audit clauses (Warden)
"Spec mechanism OR evidenced equivalent" defeats a security contract if the equivalent authorizes the same write through a different **unaudited** path while passing an outcome test. **Carve security/authz/audit/provenance clauses OUT of the outcome-equivalence escape hatch** (§10.2 Gate exclusivity, §10.4 single-use/Ledger-consumption, §16 audit completeness, §26 mandatory-provenance, §20 CAK structural exclusion). Note: G2 Security is already PROVEN-FOR-SCOPE (CORPUS/11, 9/9) — the issue is re-burying a prototyped-but-not-red-teamed domain in Phase 2, not "untested."

### C6 — Capture-now / non-retrofittable seams the plan omits (Warden + Orchestration + State)
- **Discriminator bits the served weights must CARRY (Warden, BLOCKER):** provenance / commit-status / deletion-tombstone. If Phase 1 doesn't mint them, Phase 2 can't retrofit a provenance-conditioned read — the weights don't carry the bit.
- **Timing/availability (Orchestration, BLOCKER, capture-now):** compile/compaction **wall-clock at 2,000-scale** + **mount-window read-block duration**. Phase-2 lock TTLs (60-min Write Lock, 2h PREPARED), idle-window N, read-availability are un-calibratable / un-buildable without these — and they exist ONLY while the GPU runs happen.
- **Crash matrix, one Phase-1 item (State):** mid-quantize power-fail (gguf is GPU-produced); mid-compile atomicity.

### C7 — The evaluation oracle must be METHOD-TYPED per probe class (Validation + Graph)
§21.4 names three methods (exact_substring / structured_field_match / judge_model_classification, **judge frozen at template commit**). The plan's monolithic "canonicalization + human-reviewed samples" doesn't map. CORE-retention=1.0 needs exact read-back over the **complete** CORE set, pass = **zero** losses (not ≥95%). **ε pass-threshold calibration (§22) is entirely untouched** — without a measured ε, every L2 threshold is a free parameter the designer picks (a tautology vector).

## Findings to DEMOTE under the typed bar (re-validation targets)
| Claim | Current | Re-grade | Why (load-bearing?) |
|---|---|---|---|
| **A1 batch-clean** | PROVEN-FOR-SCOPE | → constructive-demonstration at ONE point (3B/N≤100/single-seed) | B1 already wobbled to 91.7% at 7B. A1-clean IS the "compaction returns to clean" premise under the whole B3N hybrid — if it demotes, condition-3 + the hybrid verdict tighten. |
| **G3 Validation** | PROVEN-FOR-SCOPE | → constructive-demonstration | independence = identity-collision only; Reflexion fix-step stubbed; storage-truth leg = index-from-intent, not deployed store. |
| **k≤1 §8.7** | guardrail | keep as fail-closed SENTINEL | per-relation count is explicitly NOT the causal var; 3B-only, held-out-dependent. Don't inflate to "the calibrated threshold." |
| **T2.5/A5 compaction-regression** | ✅ maps directly | → COVERED-WEAK / MIS-TARGETED | n=18/n=6, no importance stratification, no CORE=1.0 abort exercised, no bystander coverage, no CompactionProbeReport structure. |
| **CP2 "L1 SELECT delivered"** | delivered | → at risk | over an intent-derived index, not the deployed store = L2 wearing an L1 label. |

## The central tension map
**The plan's two clean separations both break:**
1. **"Read co-equal, Write re-grade" ⟂ MEMIT:** Write isn't finished (C4 — 3 hard gates). Reframe: Phase 1 = **both** read-contract design AND write-engine scale gates, on a **shared stimulus-pool infrastructure**.
2. **"Defer governance to Phase 2" ⟂ State + Warden + Orchestration:** compaction-CORE-at-scale is model-coupled (C3); discriminator-bits + timing are capture-now/non-retrofittable (C6). Reframe: Phase 1 = "memory-contract substrate **+ every capture-now/non-retrofittable seam**", seam register a co-equal deliverable carrying timing/availability + discriminator-bits + bystander-probe, not just behavioral seams.

## Gate verdict (BLOCKERS to close in the plan before it's runnable)
1. Commit to a **SELECT primitive distinct from INFER** + split L1-verify-SELECT from query-surface-SELECT (C1).
2. Elevate **negative reads** to the first read falsifier, scored as a confabulation rate (C2).
3. Make **compaction-CORE-retention-at-scale over the bystander population** the top risk-ranked falsifier; build the stimulus pool; 2D N×C grid + single-solve-at-scale (C3, C4).
4. Add the **3 write-engine hard gates** (ceiling-curve, forgetting-at-scale, compaction-Component-1) co-equal with Read on the shared pool (C4).
5. **Carve security/authz/audit/provenance OUT of outcome-equivalence**; make the seam register emit **discriminator bits** (provenance/commit-status/deletion-tombstone) in Phase 1 (C5, C6).
6. Make the seam register **bind timing/availability** (compile/compaction wall-clock @2,000, mount-window read-block) — capture-now (C6).
7. **Method-type the evaluation oracle** per §21.4; CORE=1.0 = exact, zero-loss; schedule **ε calibration (§22)** (C7).
8. Execute the **demotions** above as the findings-validation pass (re-grade, don't presence-check).

## Top risk-ranked falsifier (council, for the plan's priority order)
1. **Compaction-CORE-retention-at-scale over bystanders** — already cracking (D20), kills the most contracts (Orchestration nomination; State + MEMIT concur). Cheapest path to a NOT-READY verdict if one is coming.
2. **Read contract: SELECT-primitive + negative reads** — biggest untested surface, the real "is it a database" test (Graph + Codex), but a coverage hole, not yet failing. Build in parallel; gated on resolving the SELECT-primitive question first.
