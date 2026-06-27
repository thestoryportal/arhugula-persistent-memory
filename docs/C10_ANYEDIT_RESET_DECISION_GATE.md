# C10 AnyEdit Reset — F1 Decision Gate

**Status:** pre-experiment decision gate for a fresh AnyEdit arc.
**Proposed Decision-ID:** `D-C10j-anyedit-reset`.
**Date:** 2026-06-27.
**Advisor:** Claude via `tools/claude_advisor.sh` returned `FIX-FIRST`; this
gate implements the requested fix-first scope check before any Phase-0 design.

## Purpose

This gate prevents the AnyEdit reset from optimizing for an edit-method win instead
of the F1 readiness determination.

C10 matters because project-coined multi-word semantic values fail the current
in-weight write-and-serve path. However, the spec and B3 decision already make
weights a serving copy rather than the sole authoritative store. Therefore a C10
failure does not automatically block production viability; it changes the product
contract toward a bounded hybrid.

## Binding F1 Question

Can the fixed target (`local Intel CPU + batch writes`) support project-coined
multi-word semantic values in the in-weight serving layer, or must those values
be routed through Git / `.vindex` / index / side-store mechanisms?

## Decision Meaning

### Clean AnyEdit PASS

A clean pass means:

- source-faithful AnyEdit controls recover A1/A2 before A7;
- hard A7 reaches the preregistered held-out full-sequence criterion;
- locality and bystander controls remain viable;
- the result survives advisor review and experiment-gate handoff.

F1 effect: upgrades the current write-and-serve scope from bounded hybrid toward
`in-weight-viable-with-AnyEdit` for this tested tuple. It does not close the
read/query, governance, security, deletion, pruning, or scale conditions.

### AnyEdit FAIL or HALT

A valid fail or clean halt means:

- this AnyEdit route does not rescue C10 at the tested tuple, or the port cannot
  recover source-faithful A1/A2 controls within one localized fix.

F1 effect: does not by itself make the spec unimplementable. It supports the
bounded contract: keep in-weight CORE values to single-token / prior-coherent /
empirically verified classes, and route project-coined multi-word semantic values
through Git, `.vindex`, the index, or another governed side-store.

### Invalid Result

Invalid if:

- A1/A2 controls fail;
- LAW#5 inertness fails;
- active trace is not source-faithful;
- the result is only canonical-fit or context-prefix success;
- paths/artifacts are not namespaced away from C10h.

F1 effect: no scientific update. Diagnose the method port only.

## Required Order

1. Write a fresh prereg under `D-C10j-anyedit-reset`.
2. Run Claude advisor review before harness authoring.
3. Build source-faithful A1/A2 active parity only.
4. Require A1/A2 recovery before any A7.
5. Allow one localized fix, then halt if controls still fail.
6. Only then preregister/run the hard A7 pilot with controls.
7. Run Claude advisor review before verdict.
8. Use `tools/experiment_gate.py bundle` and normal closeout before any claim.

## Bias Rule

Prior C10h results may define guardrails against known harness failure, but must
not choose thresholds, implementation shortcuts, or success interpretation.

The default/null architecture is the bounded hybrid. AnyEdit is an optional
upgrade attempt unless the spec is later amended to require project-coined
multi-word semantic values to live directly in weights.
