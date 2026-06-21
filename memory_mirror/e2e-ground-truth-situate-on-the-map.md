---
name: e2e-ground-truth-situate-on-the-map
description: "BINDING (operator-mandated 2026-06-21): docs/SPEC_E2E_GROUND_TRUTH.md is the whole-system LLM-as-DB framework + production memory lifecycle. Before EVERY experiment, hypothesis, and decision, situate it on the e2e map — which layer/cell does this touch, what does the full framework prescribe? Our work has been write-engine-centric and repeatedly lost whole-system scope; this is the standing guard."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

**`docs/SPEC_E2E_GROUND_TRUTH.md`** is the spec-faithful end-to-end picture (six layers + the production memory-management lifecycle: accumulate overlays → track drift → compact to a clean anchor + Pruning GC + behavioral-probe gates), with a §J empirical overlay (proven/amended/open).

**The finding that prompted this (operator, 2026-06-21):** our experimentation has been **write-engine-centric** — deep on MEMIT in-weight corruption (§8 + the §8.7/§11.14 drift-compaction slice), shallow-or-absent on the rest of the e2e: the **read/query contract (CP2)**, Validation/Security/2PC (prototyped-not-tested), and **Pruning/GC/out-of-band reconciliation** (≈untouched, yet half of production memory management). Symptoms of the lost scope: this session I framed the deployment write-profile as "an open operator fork" when §8.3/§8.7/§8.10 settled it (the operator had to redirect me to the spec); the late realization it's a *compaction-bounded hybrid*; the "read contract is the biggest gap" discovery.

**How to apply (BINDING):** before any experiment / hypothesis / decision, **read/recall the ground truth and name which layer/cell of the e2e framework it touches and what the full framework prescribes for it** — THEN proceed. Pairs with the SPEC-FIRST + RESEARCH-FIRST rules ([[research-first-and-verify-tool-availability]]). Wired into the re-ground read-order in `CLAUDE.md`, `DISCIPLINE.md` §1, `EXPERIMENT_RUNBOOK.md` §0.1/§1. Keep §J (the empirical overlay) current at close-out. The guard exists to stop treating one cell (the write engine) as the whole system — which silently scoped the F1 determination.
