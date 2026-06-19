# 12 — G3: DETERMINISTIC VALIDATION PIPELINE (result)
_Run 2026-06-18 on the pod. Artifacts: `/workspace/experiments/governance/g3_validation_pipeline.py`; result `/workspace/results/g3_result.json`; ledger `/workspace/results/g3_state_ledger.jsonl`. Reuses G2's Ed25519 + hash-chained ledger (components compose). Gates patches BEFORE the CP1/G1 write path._

## The G3 question (from 00 §Known Gaps / 03 + CP2)
Deterministic pre-commit patch validation, Reflexion loop, sandbox, actor-critic independence (§9) —
UNTESTED. **And CP2 surfaced two contracts as OUR-layer build items:** the L1 storage-probe triple
read-back (§8.9) and `violates`/undeclared-relation rejection (C5/C6/C9) — which LARQL does not enforce.
G3 delivers both, deterministically, plus the §9 Validation Layer.

## The solid core (lead here)
A **deterministic, non-reasoning** schema/static validator that, **before MEMIT**, rejects `violates`
(C6/C9) and undeclared relations (C5) against the **real §7.3 five-family vocabulary** — the exact
contracts CP2 proved LARQL does not enforce (CP2 found 24,469 emergent labels ≠ the 5 families). This is
the genuine CP2 closure and it cannot tautologize: the check is real logic over a real vocabulary.

## Measurement → verdict (all 8 PASS; `g3_result.json`)
| Test | What it proves | Result |
|---|---|---|
| **T-SCHEMA** (CP2 closure, core) | `violates`→`VIOLATES_REJECTED` (C6/C9); undeclared `capital_of`→`UNDECLARED_RELATION` (C5); declared `depends_on` (real §7.3) passes — all before MEMIT | all hold | ✅ |
| **T-STORAGE-PROBE** (CP2 closure, split) | (a) **expressibility**: triple `SELECT` returns a written edge, unwritten→empty (LARQL couldn't express this); (b) **storage-truth**: index says (France,assoc,Berlin) but behavioral says Paris → **storage-pass/behavior-fail detected** (§8.9 named mode) | all hold | ✅ |
| **T-INDEPENDENCE** (§9.2) | validator==author → `INDEPENDENCE_VIOLATION_VALIDATOR`; tga==coder → `INDEPENDENCE_VIOLATION_TGA` (identity collision) | both hold | ✅ |
| **T-CASCADE** (§9.3 fail-fast) | a STATIC failure → PROBE/CROSS_AGENT **not invoked** (`levels_run==["STATIC"]`); clean CORE → all three | both hold | ✅ |
| **T-CODE-PASS-PATCH-FAIL** (§9.7) | code-good package + **real** patch fault → **no PASS issued**, annotated `code_pass_patch_fail`; code-good + clean patch → passes (refusal is the patch's doing, atomic unit C-TPC1) | all hold | ✅ |
| **T-INJECTION** (§9.8) | instruction-like entity name → `INJECTION_SUSPECT` hard reject, `no_retry=True` (C29) | both hold | ✅ |
| **T-RETRY-CONTROL** (§9.5/9.6) | Tier1≤2/Tier2≤3/Tier3≤1-then-escalate; **5-event hard cap** (C27); constitutional→Tier3 (C25); budget-remaining → RETRY (not premature escalate); **no silent discard** (C28) | all hold | ✅ |
| **T-PASS-HANDOFF** (§9.9, behavioral) | downstream executor admits a **signature-valid** validator PASS; a **forged** PASS (tampered claim) and an **unsigned** PASS are refused; validator has no `.vindex` write path | all hold | ✅ |

## What G3 PROVES (precise)
- **The two CP2-surfaced contracts are delivered deterministically at OUR layer:** `violates`/undeclared
  rejection against the real §7.3 families (before MEMIT), and a triple-`SELECT` storage probe that is both
  *expressible* (LARQL couldn't) and *reconcilable* against a behavioral signal to catch storage-pass/
  behavior-fail (the actual §8.9 job).
- **The §9 Validation Layer invariants hold:** actor-critic identity separation, fail-fast cascade ordering,
  the `code_pass_patch_fail` atomic disposition, injection hard-reject-never-retry, and a bounded,
  terminating, never-silent-discard retry/escalation control-plane.
- **The §9.9 signed-signal handoff is behavioral, not asserted:** the validator's authority is a signed PASS;
  a forged or unsigned PASS is refused by the downstream executor gate. This lands G3→CP1 the way G2→G1 did.

## Honest scope / caveats (advisor-shaped; kept flush with tests)
- **Storage probe is SPLIT.** Expressibility is real CP2 closure. Storage-TRUTH is NOT carried by the index
  alone — the index is **intent-derived** (from the `.larql` parse); the divergence test works only by
  reconciling against a BEHAVIORAL signal (CP1's domain). The index is an expressibility/intent layer, not
  storage-truth.
- **Reflexion = deterministic CONTROL-PLANE only** (bounds, hard cap, escalation, termination). The LLM
  "fix" step is OUT of the deterministic core (stubbed/opaque). Claim = control-plane proven deterministic,
  NOT "Reflexion proven".
- **Actor-critic independence = identity-collision tested.** "TGA reads spec-only / enforced by sequencing"
  (D33) is **construction-asserted**, not a behavioral test (v2 enforcement-mechanism question).
- **Only the STATIC cascade level is fully real;** PROBE/CROSS_AGENT/HUMAN are stubbed/modeled (fail-fast
  ORDERING is what's tested).
- **Determinism is a documented property** (pure function, no RNG), NOT an independent finding — demoted from
  the verdict (contrast CP1, where cross-process determinism was a real falsifiable result).
- **Validator no-write** = structural (no `.vindex` method) + behavioral (forged PASS refused downstream).

## Net + a flag for the next step
G3 is **PROVEN for its scope**: a deterministic schema/validation core that delivers the two CP2-surfaced
contracts and the §9 invariants, with the signed-PASS handoff integrating G3→CP1. Carried forward: real
Reflexion fix-step + sandbox, sequencing-enforced independence, real behavioral PROBE (CP1's serve).

**Category flag (carried into G6/G7):** CP1–G3 share a shape — *we wrote code implementing a contract and
verified it implements the contract* (legitimate design-viability work, but the weaker-than-empirical
category the bootstrap names, with low real-failure risk). **G6/G7 is categorically different** — real
GGUF-Q4_K, larger Qwen3, overlay size at scale, multi-token robustness, the CP3 C15 band — these can
*actually fail*. Pass criteria MUST be set BEFORE the runs; that is where binding falsification evidence lives.
