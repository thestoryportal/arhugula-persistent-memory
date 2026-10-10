# 10 — G1: DUAL-MEDIUM 2PC + STATE LEDGER + TRANSACTION CONTROLLER + CIRCUIT BREAKER (result)
_Run 2026-06-18 on the pod. Artifacts: `/workspace/experiments/governance/g1_two_phase_commit.py`; result `/workspace/results/g1_result.json`; ledger `/workspace/results/g1_state_ledger.jsonl`; log `/workspace/logs/g1_run.log`. Git + LARQL UNMODIFIED. Builds on CP1; supplies the dual-medium atomicity CP1 deferred._

## The G1 question (from 00 §Known Gaps / 03)
CP1 proved governed in-pipeline PARAMETRIC write + clean-fail on the `.vindex` side only. G1 adds the
**second medium (Git)** and the spec's consistency machinery: **§11.5 2PC with D46 ordering**, the
**State Ledger as consistency substrate** (Git↔overlay pairing), **§11.7 Transaction Controller** (sole
compensator; C-TC2 direction-by-classification), and the **§11.8 circuit breaker** (D48).

## Method
Two **real** mediums: a real Git repo (code + `.larql` = syntactic) and the `.vindex` (frozen base +
an active-overlay pointer whose atomic flip is the parametric commit point). Reuses CP1's hash-chained
ledger and the CP1 France→Berlin overlay. **The new thing under test is the transaction machinery** —
so failure/divergence tests INJECT faults or corrupt a medium out-of-band; only the happy path and the
dual rollback run a REAL `larql APPLY+COMPILE` mount. Every claim is a test built to fail.

## Measurement → verdict (all 10 PASS; `g1_result.json`)
| Test | Falsifiable criterion | Result |
|---|---|---|
| **T-HAPPY** | PREPARE → git FIRST → vindex mount SECOND → COMMITTED binds (git_commit↔overlay_hash); serves edit | COMMITTED; real APPLY+COMPILE; served **"Berlin."**; ledger pair present | ✅ |
| **T-D46** | git-first step FAILS → `.vindex` **never attempted** → clean abort, active pointer unchanged (Weights-ahead unreachable) | `ABORTED_GIT_FIRST`, `vindex_attempted=False`, active unchanged | ✅ |
| **T-COMP-STRUCT** | Structural + mount fail → ≤3 retries → TC **auto git-revert**; no COMMITTED | git back to baseline; `COMPENSATION_COMPLETED`; no commit | ✅ |
| **T-COMP-L4** | Layer4 + mount fail → ≤5 retries → **PARK, NO auto-revert**; operator-confirm then reverts (C-TC2 asymmetry + HIL) | parked git-ahead; no auto-revert; operator revert returns to baseline | ✅ |
| **T-ROLLBACK-DUAL** | COMMITTED → dual rollback (git-revert + vindex→base) → base serves original | git rolled back; `active is None`; base serves **"Paris."** | ✅ |
| **T-DIVERGE** | out-of-band git commit (§11.13) AND vindex-pointer flip → DIVERGED → immediate trip | both detected (`side: git`/`vindex`); both breakers `CIRCUIT_TRIPPED` | ✅ |
| **T-PARK-NOT-DIVERGE** | a sanctioned Layer4 park (git-ahead) must NOT false-trip the divergence check | reconcile not diverged; no `DIVERGED_STATE` entry | ✅ |
| **T-CIRCUIT** | 3 consecutive fails → trip → READ_ONLY → new write rejected → **both reset precondition arms gate** → resume | trip logged; write rejected; bad-comp + bad-overlay resets refused; good reset admitted; resumed COMMITTED | ✅ |
| **T-LEDGER** | every 2PC emitted PREPARED; chain intact | chain intact; all COMMITTED have PREPARED | ✅ |
| **T-TPC4** | a fabricated COMMITTED with **no matching PREPARED is DETECTED** (C-TPC4 bypass) | detector flags `smuggled`, not `legit` | ✅ |

## What G1 PROVES (precise)
- **D46 ordering makes Weights-ahead structurally unreachable:** the parametric commit point is the atomic
  active-pointer flip, which happens only on full mount success; a git-first failure never touches `.vindex`,
  and a mount failure leaves no active overlay. Failures are confined to the recoverable **Git-ahead** state.
- **The C-TC2 compensation asymmetry holds, including the HIL boundary:** Structural auto-reverts Git;
  Layer4_domain **parks for human confirmation and does not auto-revert** — the operator-gated path. The TC is
  the **sole** compensator (the executor has no revert path).
- **The State Ledger is a working consistency substrate:** COMMITTED entries bind (git_commit ↔ overlay_hash);
  reconciliation detects both git-side and vindex-side divergence and trips `DIVERGED_STATE`, while a
  **sanctioned in-flight park is correctly excluded** from false-tripping (§11.8.1).
- **Circuit breaker + precondition-checked resumption:** 3-consecutive trip → READ_ONLY → writes refused;
  resumption requires BOTH reset preconditions (compensation completed AND overlay == last COMMITTED).
- **C-TPC4 bypass is DETECTED**, not merely avoided by construction: a COMMITTED lacking a PREPARED is flagged.

## Honest scope / caveats (claims kept flush with tests)
- **Compensation in the 2PC-failure path reverts GIT ONLY** — `.vindex` is written second, so on failure it
  was never mounted (nothing to revert). The `.vindex`-side reversal is exercised SEPARATELY by T-ROLLBACK-DUAL.
- **Divergence detection is ASYMMETRIC:** git side = real content (`git rev-parse HEAD` ≠ recorded commit);
  vindex side = **metadata consistency** (active-pointer's self-reported `overlay_hash` ≠ ledger field), NOT
  artifact integrity (the overlay is not re-hashed). Content-level vindex integrity → G2/G6.
- **T-ROLLBACK-DUAL serves `FROZEN_BASE` directly** (immutable; always Paris). It proves the composition
  "pointer removed AND base independently serves original," NOT an end-to-end serve-through-the-resolver.
- **Reset = precondition-checked stub** for the full IC-TC-RESET CeremonyToken/CAK flow (§11.8.1) → G2/v2
  (both precondition arms now exercised).
- **DEFERRED / UNTESTED:** PREPARED-timeout (§11.5.1, 2hr) untestable in a prototype; cross-task 5-in-10min
  trip path coded but untested (headline exercises 3-consecutive); "no self-compensate" is
  construction-asserted (not in the verdict). Mount uses the reused CP1 overlay (no recompile) — the new
  thing here is the transaction machinery, not the compile (CP1-banked).

## Net
G1 is **PROVEN for its scope**: dual-medium 2PC with D46 ordering (Weights-ahead unreachable), the C-TC2
compensation asymmetry incl. the Layer4 HIL park, a working Git↔overlay State-Ledger pairing with
divergence detection (sanctioned-park-aware), circuit-breaker trip + precondition-gated resumption, and
C-TPC4 bypass detection. Carried forward: asymmetric→content-level vindex integrity (G2/G6), the full
signed reset ceremony (G2), PREPARED-timeout + cross-task trip (later hardening). This closes the
consistency gap G1 named; G2 (security hardening) and G3 (validation pipeline) follow.
