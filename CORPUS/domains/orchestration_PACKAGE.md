# PACKAGE — 🔀 Orchestration Comparativist
_Run under COUNCIL_PROTOCOL.md. Audit vs CORPUS 05 §Orchestration. Concern: does an orchestrator satisfy all reqs; what breaks on the hardest workflow. Primary stake in workstreams #2 (migration) and #3 (pre-mortem)._

## Your spec contract (audit baseline)
Single Orchestrator-mediated control plane over six layers; review queues; lock/hold registry; Path-conditional deployment Path A (LangGraph) / B (SDK) / C (Hybrid), operator-selected (GAP-4/56/57/58); must support 2PC coordination, human-in-the-loop, audit-trail emission, concurrency model.

## Relevant evidence / context (cite from 01 + 04)
- The validated WRITE path is OFFLINE-GPU (covariance compute + AlphaEdit edit), the SERVE/READ path is CPU (LARQL). Edit-time/inference-time are SEPARABLE (04).
- Deployment target = operator's local Intel CPU; the existing **custom agent harness** is the integration target (workstream #2).
- The bridge is a discrete pipeline: edited-weights → `build_vindex_overlay.py` → `.vlp` → `larql APPLY`+`COMPILE` → serve. These are the orchestration steps to coordinate.
- Toolchain dependencies + traps (04) are orchestration constraints (transformers 4.51 pin, LARQL build deps, thread caps, tmpfs vs network-FS, Metal-vs-CPU).

## Standing questions to adversarially answer
1. **Requirement-to-capability mapping**: given the surfaced reqs (2PC [State], authz/Gate [Warden], Reflexion/Validator [Validation], MEMIT-compile [MEMIT], query schema [Graph]), can the operator's existing custom harness coordinate them — or what's missing?
2. **The hardest workflow**: a governed write = author `.larql` → validate (Reflexion) → authorize (Gate/token) → MEMIT-compile (offline GPU) → 2PC-commit (Git+.vindex+Ledger) → serve (CPU). Which steps cross the GPU/CPU boundary, and how is that orchestrated locally?
3. **HIL + audit emission**: does the harness support human-in-the-loop gates + audit-trail emission the other domains require?
4. **Migration shape (feeds #2)**: directory/harness structure, where edit-time vs serve-time live, what the Claude Code CLI workspace harness must contain.

## Seeded role: you primarily inform workstream #2 (local migration runbook) and #3 (pre-mortem). In the #1 audit, your verdict is mostly: "these reqs exist; orchestration is DEFER-TO-LOCAL design, not a viability BLOCKER — UNLESS an orchestration capability is missing that makes a domain contract unsatisfiable."
